"""Schema 모듈."""
from .config import SchemaConfig
from .interfaces import ValidationResult, FileLoader, JsonValidator, ErrorHandler
from .implementations import DefaultFileLoader, DefaultJsonValidator, DefaultErrorHandler
from .validator import SchemaValidator
from .generator import LogSchemaGenerator
from .log_validator import LogFileValidator
from .models import EventSchema, PropertyInfo, DomainInfo
from .property_builder import PropertyBuilder

# 하위 호환성을 위한 기존 함수들
from .compatibility import verify_labfile, log_schema_from_labfile, verify_logfile

__all__ = [
    'SchemaConfig',
    'ValidationResult',
    'FileLoader',
    'JsonValidator', 
    'ErrorHandler',
    'DefaultFileLoader',
    'DefaultJsonValidator',
    'DefaultErrorHandler',
    'SchemaValidator',
    'LogSchemaGenerator',
    'LogFileValidator',
    'EventSchema',
    'PropertyInfo',
    'DomainInfo',
    'PropertyBuilder',
    # 하위 호환성
    'verify_labfile',
    'log_schema_from_labfile',
    'verify_logfile'
]