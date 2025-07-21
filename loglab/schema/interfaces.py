"""Schema 모듈의 인터페이스 정의."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """검증 결과를 담는 클래스."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class FileLoader(ABC):
    """파일 로딩 인터페이스."""
    
    @abstractmethod
    def load(self, file_path: str) -> str:
        """파일을 로드하여 문자열로 반환."""
        pass


class JsonValidator(ABC):
    """JSON 스키마 검증 인터페이스."""
    
    @abstractmethod
    def validate(self, data: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
        """데이터를 스키마에 대해 검증."""
        pass


class ErrorHandler(ABC):
    """에러 처리 인터페이스."""
    
    @abstractmethod
    def handle_validation_error(self, error: Exception, context: str = "") -> ValidationResult:
        """검증 에러 처리."""
        pass
    
    @abstractmethod
    def handle_file_error(self, error: Exception, file_path: str = "") -> ValidationResult:
        """파일 에러 처리."""
        pass