"""Schema 검증기 구현."""

import json
import logging
import os
from typing import Any, Dict, Optional

from loglab.util import get_schema_file_content

from .config import SchemaConfig
from .implementations import (
    DefaultErrorHandler,
    DefaultFileLoader,
    DefaultJsonValidator,
)
from .interfaces import ErrorHandler, FileLoader, JsonValidator, ValidationResult


class SchemaValidator:
    """Lab 파일 스키마 검증기."""

    def __init__(
        self,
        file_loader: Optional[FileLoader] = None,
        json_validator: Optional[JsonValidator] = None,
        error_handler: Optional[ErrorHandler] = None,
        config: Optional[SchemaConfig] = None,
    ):
        """SchemaValidator 초기화.

        Args:
            file_loader: 파일 로딩 구현체
            json_validator: JSON 검증 구현체
            error_handler: 에러 처리 구현체
            config: 설정 객체
        """
        self.file_loader = file_loader or DefaultFileLoader()
        self.json_validator = json_validator or DefaultJsonValidator()
        self.error_handler = error_handler or DefaultErrorHandler()
        self.config = config or SchemaConfig()

    def verify_labfile(
        self, lab_path: str, schema_path: Optional[str] = None
    ) -> ValidationResult:
        """Lab 파일의 구조와 내용을 JSON 스키마로 검증.

        Args:
            lab_path: 검증할 랩 파일 경로
            schema_path: 사용할 스키마 파일 경로. None이면 기본 스키마 사용

        Returns:
            ValidationResult: 검증 결과
        """
        if schema_path is None:
            schema_path = self.config.default_schema_path
        logging.info(f"Verifying lab file: {lab_path} with schema: {schema_path}")

        try:
            # 스키마 파일 로드
            try:
                if schema_path == self.config.default_schema_path:
                    # 기본 스키마의 경우 패키지 리소스에서 직접 로드
                    logging.debug(f"Loading default schema using package resources")
                    schema_content = get_schema_file_content()
                else:
                    # 사용자 지정 스키마의 경우 파일 시스템에서 로드
                    logging.debug(f"Loading schema from: {schema_path}")
                    schema_content = self.file_loader.load(schema_path)

                schema_data = json.loads(schema_content)
                logging.debug("Schema loaded successfully")
            except FileNotFoundError as e:
                return self.error_handler.handle_file_error(e, schema_path)
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in schema file: {schema_path}")
                return self.error_handler.handle_file_error(e, schema_path)
            except Exception as e:
                logging.error(f"Failed to load schema file: {schema_path}")
                return self.error_handler.handle_validation_error(e, schema_path)

            # Lab 파일 로드 및 검증
            try:
                logging.debug(f"Loading lab file from: {lab_path}")
                lab_content = self.file_loader.load(lab_path)
                lab_data = json.loads(lab_content)
                logging.debug("Lab file loaded successfully")
            except FileNotFoundError as e:
                return self.error_handler.handle_file_error(e, lab_path)
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in lab file: {lab_path}")
                return self.error_handler.handle_file_error(e, lab_path)

            # 재귀적 검증 수행
            return self._recursive_validate(lab_data, schema_data, lab_path)

        except Exception as e:
            return self.error_handler.handle_validation_error(e, lab_path)

    def _recursive_validate(
        self, lab_data: Dict[str, Any], schema_data: Dict[str, Any], lab_path: str
    ) -> ValidationResult:
        """Lab 파일과 그것이 import하는 모든 파일들을 재귀적으로 검증.

        Args:
            lab_data: 검증할 lab 파일 데이터
            schema_data: 검증에 사용할 JSON 스키마
            lab_path: lab 파일의 경로 (에러 메시지용)

        Returns:
            ValidationResult: 검증 결과
        """
        try:
            # import하는 파일들도 검증
            if "import" in lab_data:
                basedir = os.path.dirname(lab_path)
                for imp in lab_data["import"]:
                    import_path = os.path.join(basedir, f"{imp}.lab.json")

                    try:
                        logging.debug(f"Importing file: {import_path}")
                        import_content = self.file_loader.load(import_path)
                        import_data = json.loads(import_content)

                        # 재귀적으로 import된 파일도 검증
                        result = self._recursive_validate(
                            import_data, schema_data, import_path
                        )
                        if not result.success:
                            # import된 파일에서 에러가 발생하면 컨텍스트 추가
                            result.errors = [
                                f"In imported file {import_path}: {error}"
                                for error in result.errors
                            ]
                            return result

                    except Exception as e:
                        return self.error_handler.handle_validation_error(
                            e, f"importing {import_path} from {lab_path}"
                        )

            # 현재 파일 검증
            return self.json_validator.validate(lab_data, schema_data)

        except Exception as e:
            return self.error_handler.handle_validation_error(e, lab_path)
