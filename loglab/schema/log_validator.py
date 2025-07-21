"""로그 파일 검증기."""
import json
import copy
from collections import defaultdict
from typing import Dict, Any, List

from jsonschema import validate, ValidationError

from .interfaces import ValidationResult, ErrorHandler
from .implementations import DefaultErrorHandler
from .config import SchemaConfig


class LogFileValidator:
    """로그 파일 검증기 클래스."""
    
    def __init__(
        self,
        error_handler: ErrorHandler = None,
        config: SchemaConfig = None
    ):
        """LogFileValidator 초기화.
        
        Args:
            error_handler: 에러 처리기
            config: 설정 객체
        """
        self.error_handler = error_handler or DefaultErrorHandler()
        self.config = config or SchemaConfig()
    
    def validate_logfile(self, schema_path: str, log_path: str) -> ValidationResult:
        """실제 로그 파일이 생성된 스키마에 맞는지 검증.
        
        Args:
            schema_path: 로그 검증용 JSON 스키마 파일 경로
            log_path: 검증할 로그 파일 경로
            
        Returns:
            ValidationResult: 검증 결과
        """
        try:
            # 스키마 로드 및 파싱
            schema_data = self._load_schema(schema_path)
            if not schema_data:
                return ValidationResult(
                    success=False,
                    errors=["Failed to load schema file"]
                )
            
            # 이벤트별 스키마 생성
            event_schemas = self._create_event_schemas(schema_data)
            
            # 로그 파일 검증
            return self._validate_log_entries(log_path, event_schemas)
            
        except Exception as e:
            return self.error_handler.handle_validation_error(e, f"validating {log_path}")
    
    def _load_schema(self, schema_path: str) -> Dict[str, Any]:
        """스키마 파일을 로드하고 파싱.
        
        Args:
            schema_path: 스키마 파일 경로
            
        Returns:
            파싱된 스키마 데이터
        """
        try:
            with open(schema_path, 'rt', encoding=self.config.encoding) as f:
                content = f.read()
                return json.loads(content)
        except json.JSONDecodeError as e:
            print("Error: 로그랩이 생성한 JSON 스키마 에러. 로그랩 개발자에 문의 요망.")
            print(e)
            return None
        except Exception as e:
            print(f"Error loading schema: {e}")
            return None
    
    def _create_event_schemas(self, schema_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """전체 스키마에서 이벤트별 스키마를 생성.
        
        Args:
            schema_data: 전체 스키마 데이터
            
        Returns:
            이벤트별 스키마 딕셔너리
        """
        event_schemas = {}
        
        for ref in schema_data['items']['oneOf']:
            event_name = ref['$ref'].split('/')[-1]
            
            # 각 이벤트용 스키마 생성 (다른 이벤트는 제거)
            event_schema = copy.deepcopy(schema_data)
            event_schema['$defs'] = {event_name: schema_data['$defs'][event_name]}
            event_schema['items'] = ref
            
            event_schemas[event_name] = event_schema
        
        return event_schemas
    
    def _validate_log_entries(
        self, 
        log_path: str, 
        event_schemas: Dict[str, Dict[str, Any]]
    ) -> ValidationResult:
        """로그 엔트리들을 검증.
        
        Args:
            log_path: 로그 파일 경로
            event_schemas: 이벤트별 스키마
            
        Returns:
            ValidationResult: 검증 결과
        """
        try:
            # 로그 파일 파싱 및 이벤트별 분류
            log_entries = self._parse_log_file(log_path, event_schemas)
            if not log_entries.success:
                return log_entries
            
            # 이벤트별로 검증 수행
            return self._validate_by_events(log_entries.data, event_schemas)
            
        except Exception as e:
            return self.error_handler.handle_validation_error(e, f"parsing {log_path}")
    
    def _parse_log_file(
        self, 
        log_path: str, 
        event_schemas: Dict[str, Dict[str, Any]]
    ) -> ValidationResult:
        """로그 파일을 파싱하고 이벤트별로 분류.
        
        Args:
            log_path: 로그 파일 경로
            event_schemas: 이벤트별 스키마
            
        Returns:
            ValidationResult: 파싱 결과
        """
        event_line_numbers = defaultdict(list)
        event_logs = defaultdict(list)
        
        try:
            with open(log_path, 'rt', encoding=self.config.encoding) as f:
                for line_no, line in enumerate(f):
                    try:
                        log_entry = json.loads(line)
                    except json.JSONDecodeError as e:
                        return ValidationResult(
                            success=False,
                            errors=[f"[Line: {line_no + 1}] 유효한 JSON 형식이 아닙니다: {e}"]
                        )
                    
                    # 이벤트 타입 확인
                    if 'Event' not in log_entry or log_entry['Event'] not in event_schemas:
                        return ValidationResult(
                            success=False,
                            errors=[f"[Line: {line_no + 1}] 스키마에서 이벤트를 찾을 수 없습니다: {line.strip()}"]
                        )
                    
                    event_name = log_entry['Event']
                    event_line_numbers[event_name].append(line_no)
                    event_logs[event_name].append(log_entry)
            
            return ValidationResult(
                success=True,
                data={
                    'event_logs': event_logs,
                    'event_line_numbers': event_line_numbers
                }
            )
            
        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[f"Error reading log file: {e}"]
            )
    
    def _validate_by_events(
        self, 
        log_data: Dict[str, Any], 
        event_schemas: Dict[str, Dict[str, Any]]
    ) -> ValidationResult:
        """이벤트별로 로그 엔트리들을 검증.
        
        Args:
            log_data: 이벤트별로 분류된 로그 데이터
            event_schemas: 이벤트별 스키마
            
        Returns:
            ValidationResult: 검증 결과
        """
        event_logs = log_data['event_logs']
        event_line_numbers = log_data['event_line_numbers']
        
        for event_name, logs in event_logs.items():
            schema = event_schemas[event_name]
            
            try:
                validate(logs, schema=schema)
            except ValidationError as e:
                # 에러가 발생한 로그의 라인 번호 찾기
                error_index = list(e.absolute_path)[0]
                line_no = event_line_numbers[event_name][error_index]
                error_log = logs[error_index]
                
                return ValidationResult(
                    success=False,
                    errors=[f"[Line: {line_no + 1}] {e.message}: {json.dumps(error_log, ensure_ascii=False)}"]
                )
        
        return ValidationResult(success=True)