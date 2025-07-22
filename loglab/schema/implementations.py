"""Schema 인터페이스의 기본 구현체들."""

import json
import os
from typing import Any, Dict

from jsonschema import ValidationError, validate

from loglab.util import load_file_from

from .interfaces import ErrorHandler, FileLoader, JsonValidator, ValidationResult


class DefaultFileLoader(FileLoader):
    """기본 파일 로더 구현."""

    def load(self, file_path: str) -> str:
        """파일을 로드하여 문자열로 반환."""
        return load_file_from(file_path)


class DefaultJsonValidator(JsonValidator):
    """기본 JSON 스키마 검증기 구현."""

    def validate(
        self, data: Dict[str, Any], schema: Dict[str, Any]
    ) -> ValidationResult:
        """데이터를 스키마에 대해 검증."""
        try:
            validate(data, schema)
            return ValidationResult(success=True, data=data)
        except ValidationError as e:
            return ValidationResult(
                success=False, errors=[f"Validation error: {e.message}"]
            )
        except Exception as e:
            return ValidationResult(
                success=False, errors=[f"Unexpected validation error: {str(e)}"]
            )


class DefaultErrorHandler(ErrorHandler):
    """기본 에러 처리기 구현."""

    def handle_validation_error(
        self, error: Exception, context: str = ""
    ) -> ValidationResult:
        """검증 에러 처리."""
        error_msg = f"Validation error"
        if context:
            error_msg += f" in {context}"
        error_msg += f": {str(error)}"

        return ValidationResult(success=False, errors=[error_msg])

    def handle_file_error(
        self, error: Exception, file_path: str = ""
    ) -> ValidationResult:
        """파일 에러 처리."""
        if isinstance(error, FileNotFoundError):
            error_msg = f"File not found: {file_path or 'unknown'}"
        elif isinstance(error, json.JSONDecodeError):
            error_msg = f"Invalid JSON in file: {file_path or 'unknown'}"
        else:
            error_msg = f"File error: {str(error)}"

        return ValidationResult(success=False, errors=[error_msg])
