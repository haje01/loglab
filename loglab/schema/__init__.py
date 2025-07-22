"""Schema 모듈."""

# 하위 호환성을 위한 기존 함수들
from .compatibility import log_schema_from_labfile, verify_labfile, verify_logfile
from .config import SchemaConfig
from .generator import LogSchemaGenerator
from .implementations import (
    DefaultErrorHandler,
    DefaultFileLoader,
    DefaultJsonValidator,
)
from .interfaces import ErrorHandler, FileLoader, JsonValidator, ValidationResult
from .log_validator import LogFileValidator
from .models import DomainInfo, EventSchema, PropertyInfo
from .property_builder import PropertyBuilder
from .validator import SchemaValidator

__all__ = [
    "SchemaConfig",
    "ValidationResult",
    "FileLoader",
    "JsonValidator",
    "ErrorHandler",
    "DefaultFileLoader",
    "DefaultJsonValidator",
    "DefaultErrorHandler",
    "SchemaValidator",
    "LogSchemaGenerator",
    "LogFileValidator",
    "EventSchema",
    "PropertyInfo",
    "DomainInfo",
    "PropertyBuilder",
    # 하위 호환성
    "verify_labfile",
    "log_schema_from_labfile",
    "verify_logfile",
]
