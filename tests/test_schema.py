"""Schema 모듈 테스트."""
import json
import pytest
from unittest.mock import Mock, patch, mock_open

from loglab.schema import (
    SchemaValidator, LogSchemaGenerator, LogFileValidator,
    ValidationResult, DefaultFileLoader, DefaultJsonValidator, DefaultErrorHandler,
    SchemaConfig, PropertyBuilder, EventSchema, PropertyInfo, DomainInfo
)


class TestSchemaConfig:
    """SchemaConfig 테스트."""
    
    def test_default_values(self):
        """기본값 테스트."""
        config = SchemaConfig()
        assert config.encoding == "utf8"
        assert config.json_schema_version == "https://json-schema.org/draft/2020-12/schema"
        assert "^([0-9]+)-" in config.datetime_pattern


class TestValidationResult:
    """ValidationResult 테스트."""
    
    def test_success_result(self):
        """성공 결과 테스트."""
        result = ValidationResult(success=True, data={"test": "data"})
        assert result.success is True
        assert result.data == {"test": "data"}
        assert result.errors == []
    
    def test_failure_result(self):
        """실패 결과 테스트."""
        result = ValidationResult(success=False, errors=["error1", "error2"])
        assert result.success is False
        assert result.errors == ["error1", "error2"]
        assert result.data is None


class TestDefaultFileLoader:
    """DefaultFileLoader 테스트."""
    
    @patch('loglab.schema.implementations.load_file_from')
    def test_load_success(self, mock_load):
        """파일 로드 성공 테스트."""
        mock_load.return_value = "file content"
        loader = DefaultFileLoader()
        
        result = loader.load("test.json")
        
        assert result == "file content"
        mock_load.assert_called_once_with("test.json")
    
    @patch('loglab.schema.implementations.load_file_from')
    def test_load_failure(self, mock_load):
        """파일 로드 실패 테스트."""
        mock_load.side_effect = FileNotFoundError("File not found")
        loader = DefaultFileLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load("missing.json")


class TestDefaultJsonValidator:
    """DefaultJsonValidator 테스트."""
    
    def test_validate_success(self):
        """검증 성공 테스트."""
        validator = DefaultJsonValidator()
        data = {"name": "test"}
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        
        result = validator.validate(data, schema)
        
        assert result.success is True
        assert result.data == data
    
    def test_validate_failure(self):
        """검증 실패 테스트."""
        validator = DefaultJsonValidator()
        data = {"name": 123}  # 잘못된 타입
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        
        result = validator.validate(data, schema)
        
        assert result.success is False
        assert len(result.errors) > 0
        assert "Validation error" in result.errors[0]


class TestPropertyBuilder:
    """PropertyBuilder 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.builder = PropertyBuilder()
    
    def test_build_datetime_property(self):
        """datetime 속성 생성 테스트."""
        result = self.builder.build_datetime_property("created_at", "생성 시간")
        
        # 문자열 형태로 반환되는지 확인
        assert isinstance(result, str)
        assert '"created_at"' in result
        assert '"type": "string"' in result
        assert '"description": "생성 시간"' in result
        assert "pattern" in result
    
    def test_build_typed_property(self):
        """타입 속성 생성 테스트."""
        property_info = PropertyInfo(
            name="user_id",
            type="integer",
            description="사용자 ID",
            constraints={"minimum": 1, "maximum": 1000}
        )
        
        result = self.builder.build_typed_property(property_info)
        
        # 문자열 형태로 반환되는지 확인
        assert isinstance(result, str)
        assert '"user_id"' in result
        assert '"type": "integer"' in result
        assert '"description": "사용자 ID"' in result
        assert '"minimum": 1' in result
        assert '"maximum": 1000' in result
    
    def test_extract_required_fields(self):
        """필수 필드 추출 테스트."""
        fields = {
            "field1": [["", {"type": "string", "desc": "필수 필드"}]],
            "field2": [["", {"type": "integer", "desc": "선택적 필드", "option": True}]],
            "field3": [["", {"type": "string", "desc": "또 다른 필수 필드", "option": False}]]
        }
        
        required = self.builder.extract_required_fields(fields)
        
        assert "field1" in required
        assert "field2" not in required  # option=True
        assert "field3" in required


class TestSchemaValidator:
    """SchemaValidator 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.mock_file_loader = Mock()
        self.mock_json_validator = Mock()
        self.mock_error_handler = Mock()
        
        self.validator = SchemaValidator(
            file_loader=self.mock_file_loader,
            json_validator=self.mock_json_validator,
            error_handler=self.mock_error_handler
        )
    
    def test_verify_labfile_success(self):
        """lab 파일 검증 성공 테스트."""
        # Mock 설정
        self.mock_file_loader.load.side_effect = [
            '{"type": "object"}',  # schema
            '{"domain": {"name": "test"}}'  # lab file
        ]
        self.mock_json_validator.validate.return_value = ValidationResult(
            success=True, 
            data={"domain": {"name": "test"}}
        )
        
        result = self.validator.verify_labfile("test.lab.json", "schema.json")
        
        assert result.success is True
        assert self.mock_file_loader.load.call_count == 2
        self.mock_json_validator.validate.assert_called_once()
    
    def test_verify_labfile_with_imports(self):
        """import가 있는 lab 파일 검증 테스트."""
        # Mock 설정
        self.mock_file_loader.load.side_effect = [
            '{"type": "object"}',  # schema
            '{"domain": {"name": "test"}, "import": ["base"]}',  # main lab file
            '{"domain": {"name": "base"}}'  # imported lab file
        ]
        self.mock_json_validator.validate.return_value = ValidationResult(success=True)
        
        result = self.validator.verify_labfile("test.lab.json", "schema.json")
        
        assert result.success is True
        assert self.mock_file_loader.load.call_count == 3


class TestLogSchemaGenerator:
    """LogSchemaGenerator 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.mock_property_builder = Mock()
        self.generator = LogSchemaGenerator(property_builder=self.mock_property_builder)
    
    @patch('loglab.schema.generator.build_model')
    def test_generate_schema_basic(self, mock_build_model):
        """기본 스키마 생성 테스트."""
        # Mock 모델 데이터
        mock_domain = Mock()
        mock_domain.domain.name = "test"
        mock_domain.domain.desc = "테스트 도메인"
        mock_domain.events = {
            "Login": [["", {"fields": {"user_id": [["", {"type": "integer", "desc": "사용자 ID"}]]}}]]
        }
        mock_build_model.return_value = mock_domain
        
        # Mock property builder (문자열 리스트 반환)
        self.mock_property_builder.build_properties_from_fields.return_value = [
            '"user_id": {"type": "integer", "description": "사용자 ID"}'
        ]
        self.mock_property_builder.extract_required_fields.return_value = ["user_id"]
        
        result = self.generator.generate_schema({"test": "data"})
        
        # 결과 검증 (문자열 형태로 반환됨)
        assert isinstance(result, str)
        assert "test" in result
        assert "테스트 도메인" in result
        assert "Login" in result
        assert "$defs" in result


class TestLogFileValidator:
    """LogFileValidator 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.validator = LogFileValidator()
    
    def test_load_schema_success(self):
        """스키마 로드 성공 테스트."""
        schema_data = {"items": {"oneOf": []}, "$defs": {}}
        
        with patch("builtins.open", mock_open(read_data=json.dumps(schema_data))):
            result = self.validator._load_schema("schema.json")
        
        assert result == schema_data
    
    def test_load_schema_invalid_json(self):
        """잘못된 JSON 스키마 로드 테스트."""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with patch("builtins.print"):  # print 출력 무시
                result = self.validator._load_schema("schema.json")
        
        assert result is None
    
    def test_create_event_schemas(self):
        """이벤트별 스키마 생성 테스트."""
        schema_data = {
            "items": {
                "oneOf": [
                    {"$ref": "#/$defs/Login"},
                    {"$ref": "#/$defs/Logout"}
                ]
            },
            "$defs": {
                "Login": {"type": "object"},
                "Logout": {"type": "object"}
            }
        }
        
        result = self.validator._create_event_schemas(schema_data)
        
        assert "Login" in result
        assert "Logout" in result
        assert result["Login"]["$defs"] == {"Login": {"type": "object"}}
        assert result["Logout"]["$defs"] == {"Logout": {"type": "object"}}


class TestCompatibilityFunctions:
    """하위 호환성 함수들 테스트."""
    
    @patch('loglab.schema.compatibility.SchemaValidator')
    def test_verify_labfile_compatibility(self, mock_validator_class):
        """verify_labfile 호환성 테스트."""
        from loglab.schema.compatibility import verify_labfile
        
        # Mock 설정
        mock_validator = Mock()
        mock_validator.verify_labfile.return_value = ValidationResult(
            success=True, 
            data={"test": "data"}
        )
        mock_validator_class.return_value = mock_validator
        
        result = verify_labfile("test.lab.json")
        
        assert result == {"test": "data"}
        mock_validator.verify_labfile.assert_called_once_with("test.lab.json", None)
    
    @patch('loglab.schema.compatibility.LogSchemaGenerator')
    def test_log_schema_from_labfile_compatibility(self, mock_generator_class):
        """log_schema_from_labfile 호환성 테스트."""
        from loglab.schema.compatibility import log_schema_from_labfile
        
        # Mock 설정
        mock_generator = Mock()
        mock_generator.generate_schema.return_value = '{"test": "schema"}'
        mock_generator_class.return_value = mock_generator
        
        result = log_schema_from_labfile({"test": "data"})
        
        assert result == '{"test": "schema"}'
        mock_generator.generate_schema.assert_called_once_with({"test": "data"})