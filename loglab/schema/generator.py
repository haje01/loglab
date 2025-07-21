"""로그 스키마 생성기."""
import json
from typing import Dict, Any, List

from loglab.model import build_model
from loglab.util import AttrDict

from .models import EventSchema, DomainInfo
from .property_builder import PropertyBuilder
from .config import SchemaConfig


class LogSchemaGenerator:
    """로그 스키마 생성기 클래스."""
    
    def __init__(
        self, 
        property_builder: PropertyBuilder = None,
        config: SchemaConfig = None
    ):
        """LogSchemaGenerator 초기화.
        
        Args:
            property_builder: 속성 빌더
            config: 설정 객체
        """
        self.config = config or SchemaConfig()
        self.property_builder = property_builder or PropertyBuilder(self.config)
    
    def generate_schema(self, lab_data: Dict[str, Any]) -> str:
        """lab 파일 데이터로부터 실제 로그 검증용 JSON 스키마를 생성.
        
        Args:
            lab_data: 빌드된 lab 모델 데이터
            
        Returns:
            JSON 형태의 로그 검증 스키마 문자열
        """
        # 모델 빌드
        domain_model = build_model(lab_data)
        
        # 도메인 정보 추출
        domain_info = DomainInfo(
            name=domain_model.domain.name,
            description=domain_model.domain.desc
        )
        
        # 이벤트 스키마들 생성
        event_schemas = self._process_events(domain_model.events)
        
        # 최종 스키마 조립
        return self._assemble_schema(domain_info, event_schemas)
    
    def _process_events(self, events: Dict[str, Any]) -> List[EventSchema]:
        """이벤트들을 처리하여 EventSchema 리스트로 변환.
        
        Args:
            events: 이벤트 정보 딕셔너리
            
        Returns:
            EventSchema 리스트
        """
        event_schemas = []
        
        for event_name, event_list in events.items():
            event_data = AttrDict(event_list[-1][1])
            event_schema = self._build_event_schema(event_name, event_data)
            event_schemas.append(event_schema)
        
        return event_schemas
    
    def _build_event_schema(self, event_name: str, event_data: AttrDict) -> EventSchema:
        """단일 이벤트의 스키마를 생성.
        
        Args:
            event_name: 이벤트명
            event_data: 이벤트 데이터
            
        Returns:
            EventSchema 객체
        """
        # 속성들 생성 (문자열 리스트로)
        property_strings = self.property_builder.build_properties_from_fields(event_data.fields)
        
        # Event 속성 추가 (이벤트명을 상수로)
        event_property = f'"Event": {{"const": "{event_name}"}}'
        property_strings.append(event_property)
        
        # 필수 필드들 추출
        required_fields = self.property_builder.extract_required_fields(event_data.fields)
        
        return EventSchema(
            name=event_name,
            properties=property_strings,  # 문자열 리스트
            required_fields=required_fields,
            description=event_data.get('desc', '')
        )
    
    def _assemble_schema(self, domain_info: DomainInfo, event_schemas: List[EventSchema]) -> str:
        """도메인 정보와 이벤트 스키마들로 최종 JSON 스키마를 조립.
        
        Args:
            domain_info: 도메인 정보
            event_schemas: 이벤트 스키마 리스트
            
        Returns:
            JSON 형태의 스키마 문자열 (기존 방식과 호환)
        """
        # 이벤트별 스키마 문자열 생성
        events = []
        items = []
        
        for event_schema in event_schemas:
            # 속성들을 조합
            properties_str = ",".join(event_schema.properties)
            
            # 필수 필드들을 조합
            required_str = ", ".join([f'"{field}"' for field in event_schema.required_fields])
            
            # 이벤트 본문 생성
            event_body = f'''
            "type": "object",
            "properties": {{
                {properties_str}
            }},
            "required": [{required_str}],
            "additionalProperties": false
        '''
            
            events.append(f'"{event_schema.name}" : {{\n      {event_body}')
            items.append(f'{{"$ref": "#/$defs/{event_schema.name}"}}')
        
        events_str = '\n        },\n        '.join(events) + "}"
        items_str = ",\n            ".join(items)
        
        return f'''
{{
    "$schema": "{self.config.json_schema_version}",
    "title": "{domain_info.name}",
    "description": "{domain_info.description}",
    "type": "array",
    "$defs": {{
        {events_str}
    }},
    "items": {{
        "oneOf": [
            {items_str}
        ]
    }}
}}
    '''