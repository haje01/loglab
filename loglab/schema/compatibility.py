"""하위 호환성을 위한 기존 함수들의 래퍼."""
import sys
from typing import Dict, Any, Optional

from .validator import SchemaValidator
from .generator import LogSchemaGenerator
from .log_validator import LogFileValidator


def verify_labfile(lab_path: str, scm_path: Optional[str] = None, err_exit: bool = True) -> Optional[Dict[str, Any]]:
    """lab 파일의 구조와 내용을 JSON 스키마로 검증.
    
    기존 함수와의 하위 호환성을 위한 래퍼 함수.
    새로운 SchemaValidator 클래스를 사용하여 구현.

    Args:
        lab_path: 검증할 랩 파일 경로
        scm_path: 사용할 스키마 파일 경로. None이면 기본 스키마 사용
        err_exit: 에러 발생시 프로그램 종료 여부. 기본 True

    Returns:
        dict: 검증이 완료된 랩 파일 데이터 (성공시에만)
        
    Raises:
        SystemExit: err_exit=True이고 검증 실패시
    """
    validator = SchemaValidator()
    result = validator.verify_labfile(lab_path, scm_path)
    
    if not result.success:
        print("Error: 랩 파일 검증 에러")
        for error in result.errors:
            print(error)
        if err_exit:
            sys.exit(1)
        return None
    
    return result.data


def log_schema_from_labfile(data: Dict[str, Any]) -> str:
    """lab 파일 데이터로부터 실제 로그 검증용 JSON 스키마를 동적 생성.
    
    기존 함수와의 하위 호환성을 위한 래퍼 함수.
    새로운 LogSchemaGenerator 클래스를 사용하여 구현.

    Args:
        data: 빌드된 lab 모델 데이터
        
    Returns:
        str: JSON 형태의 로그 검증 스키마 문자열
    """
    generator = LogSchemaGenerator()
    return generator.generate_schema(data)


def verify_logfile(schema: str, logfile: str) -> None:
    """실제 로그 파일이 생성된 스키마에 맞는지 검증.
    
    기존 함수와의 하위 호환성을 위한 래퍼 함수.
    새로운 LogFileValidator 클래스를 사용하여 구현.

    Args:
        schema: 로그 검증용 JSON 스키마 파일 경로
        logfile: 검증할 로그 파일 경로
        
    Raises:
        SystemExit: 스키마 파일이 잘못되었거나 로그 검증 실패시
    """
    validator = LogFileValidator()
    result = validator.validate_logfile(schema, logfile)
    
    if not result.success:
        for error in result.errors:
            print(f"Error: {error}")
        sys.exit(1)