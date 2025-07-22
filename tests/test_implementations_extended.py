"""확장된 schema implementations 테스트."""

import json
import os
import tempfile
from unittest.mock import Mock, mock_open, patch

import pytest

from loglab.schema.implementations import (
    DefaultErrorHandler,
    DefaultFileLoader,
    DefaultJsonValidator,
)
from loglab.schema.interfaces import ValidationResult


class TestDefaultFileLoader:
    """DefaultFileLoader 확장 테스트."""

    def test_load_large_file(self):
        """대용량 파일 로드."""
        large_content = '{"data": "' + "x" * 10000 + '"}'

        with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf8") as f:
            f.write(large_content)
            temp_path = f.name

        try:
            loader = DefaultFileLoader()
            content = loader.load(temp_path)
            assert len(content) > 10000
            assert '"data":' in content
        finally:
            os.unlink(temp_path)

    def test_load_empty_file(self):
        """빈 파일 로드."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf8") as f:
            temp_path = f.name

        try:
            loader = DefaultFileLoader()
            content = loader.load(temp_path)
            assert content == ""
        finally:
            os.unlink(temp_path)

    def test_load_permission_error(self):
        """권한 에러 처리."""
        loader = DefaultFileLoader()

        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            with pytest.raises(PermissionError):
                loader.load("/restricted/file.json")


class TestDefaultJsonValidator:
    """DefaultJsonValidator 확장 테스트."""

    def test_validate_complex_schema(self):
        """복잡한 스키마 검증."""
        validator = DefaultJsonValidator()

        complex_schema = {
            "type": "object",
            "properties": {
                "events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "timestamp": {"type": "string", "format": "date-time"},
                            "data": {"type": "object"},
                        },
                        "required": ["name", "timestamp"],
                    },
                }
            },
            "required": ["events"],
        }

        valid_data = {
            "events": [
                {
                    "name": "test_event",
                    "timestamp": "2023-01-01T00:00:00Z",
                    "data": {"key": "value"},
                }
            ]
        }

        result = validator.validate(valid_data, complex_schema)
        assert result.success is True
        assert result.data == valid_data

    def test_validate_nested_validation_error(self):
        """중첩된 검증 에러."""
        validator = DefaultJsonValidator()

        schema = {
            "type": "object",
            "properties": {
                "nested": {
                    "type": "object",
                    "properties": {"required_field": {"type": "string"}},
                    "required": ["required_field"],
                }
            },
            "required": ["nested"],
        }

        invalid_data = {"nested": {"wrong_field": "value"}}

        result = validator.validate(invalid_data, schema)
        assert result.success is False
        assert len(result.errors) > 0
        assert "required_field" in result.errors[0]

    def test_validate_type_coercion_error(self):
        """타입 강제 변환 에러."""
        validator = DefaultJsonValidator()

        schema = {
            "type": "object",
            "properties": {
                "number_field": {"type": "number"},
                "string_field": {"type": "string"},
            },
        }

        invalid_data = {"number_field": "not_a_number", "string_field": 123}

        result = validator.validate(invalid_data, schema)
        assert result.success is False
        assert "not_a_number" in result.errors[0]


class TestDefaultErrorHandler:
    """DefaultErrorHandler 확장 테스트."""

    def test_handle_validation_error_with_context(self):
        """컨텍스트가 있는 검증 에러 처리."""
        handler = DefaultErrorHandler()
        error = ValueError("Invalid value")

        result = handler.handle_validation_error(error, "user_input")

        assert result.success is False
        assert "user_input" in result.errors[0]
        assert "Invalid value" in result.errors[0]

    def test_handle_validation_error_without_context(self):
        """컨텍스트가 없는 검증 에러 처리."""
        handler = DefaultErrorHandler()
        error = ValueError("Invalid value")

        result = handler.handle_validation_error(error)

        assert result.success is False
        assert "Invalid value" in result.errors[0]

    def test_handle_file_not_found_error(self):
        """파일 찾을 수 없음 에러 처리."""
        handler = DefaultErrorHandler()
        error = FileNotFoundError("File not found")

        result = handler.handle_file_error(error, "/path/to/file.json")

        assert result.success is False
        assert "File not found" in result.errors[0]
        assert "/path/to/file.json" in result.errors[0]

    def test_handle_json_decode_error(self):
        """JSON 디코드 에러 처리."""
        handler = DefaultErrorHandler()
        error = json.JSONDecodeError("Invalid JSON", "doc", 10)

        result = handler.handle_file_error(error, "config.json")

        assert result.success is False
        assert "Invalid JSON" in result.errors[0]
        assert "config.json" in result.errors[0]

    def test_handle_generic_file_error(self):
        """일반 파일 에러 처리."""
        handler = DefaultErrorHandler()
        error = PermissionError("Access denied")

        result = handler.handle_file_error(error, "restricted.json")

        assert result.success is False
        assert "Access denied" in result.errors[0]

    def test_handle_file_error_without_path(self):
        """경로 없는 파일 에러 처리."""
        handler = DefaultErrorHandler()
        error = FileNotFoundError("File not found")

        result = handler.handle_file_error(error)

        assert result.success is False
        assert "unknown" in result.errors[0]


class TestValidationResult:
    """ValidationResult 확장 테스트."""

    def test_validation_result_success_properties(self):
        """성공 결과 속성 확인."""
        result = ValidationResult(success=True, data={"key": "value"})

        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.errors == []

    def test_validation_result_failure_properties(self):
        """실패 결과 속성 확인."""
        errors = ["Error 1", "Error 2"]
        result = ValidationResult(success=False, errors=errors)

        assert result.success is False
        assert result.errors == errors
        assert result.data is None

    def test_validation_result_default_values(self):
        """기본값 확인."""
        result = ValidationResult(success=True)

        assert result.success is True
        assert result.data is None
        assert result.errors == []
