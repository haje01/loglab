"""스키마 속성 빌더."""
import json
from typing import Dict, Any, List

from .models import PropertyInfo
from .config import SchemaConfig


class PropertyBuilder:
    """스키마 속성 빌더 클래스."""
    
    def __init__(self, config: SchemaConfig = None):
        """PropertyBuilder 초기화.
        
        Args:
            config: 스키마 설정 객체
        """
        self.config = config or SchemaConfig()
    
    def build_datetime_property(self, field_name: str, description: str) -> str:
        """datetime 타입 속성을 생성.
        
        Args:
            field_name: 필드명
            description: 필드 설명
            
        Returns:
            datetime 속성 문자열 (기존 방식과 호환)
        """
        return f'''
                "{field_name}": {{
                    "type": "string",
                    "description": "{description}",
                    "pattern": "^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)(\\\\.[0-9]+)?(([Zz])|([\\\\+|\\\\-]([01][0-9]|2[0-3]):?[0-5][0-9]))$"
                }}'''
    
    def build_typed_property(self, property_info: PropertyInfo) -> str:
        """타입 정보를 기반으로 속성을 생성.
        
        Args:
            property_info: 속성 정보
            
        Returns:
            속성 문자열 (기존 방식과 호환)
        """
        field_info = {
            "type": property_info.type,
            "description": property_info.description
        }
        
        # 제약 조건들 추가
        for constraint_key, constraint_value in property_info.constraints.items():
            if constraint_key in ('type', 'desc'):
                continue
                
            if constraint_key == 'enum' and len(constraint_value) > 0:
                # enum 값들 정리
                enum_values = []
                for value in constraint_value:
                    if isinstance(value, list):
                        enum_values.append(value[0])
                    else:
                        enum_values.append(value)
                field_info['enum'] = enum_values
                
            elif constraint_key == 'const' and len(constraint_value) > 0:
                # const 값 정리
                if isinstance(constraint_value, list):
                    field_info['const'] = constraint_value[0]
                else:
                    field_info['const'] = constraint_value
                    
            else:
                field_info[constraint_key] = constraint_value
        
        body = json.dumps(field_info, ensure_ascii=False)
        return f'''
                "{property_info.name}": {body}'''
    
    def build_properties_from_fields(self, fields: Dict[str, Any]) -> List[str]:
        """필드 정보로부터 속성들을 생성.
        
        Args:
            fields: 필드 정보 딕셔너리
            
        Returns:
            속성 문자열 리스트 (기존 방식과 호환)
        """
        properties = []
        
        for field_key, field_value in fields.items():
            field_data = field_value[-1]  # 마지막 값 사용
            field_elements = field_key.split('.')
            field_name = field_elements[-1]
            field_type = field_data[1]['type']
            field_desc = field_data[1]['desc']
            
            if field_type == "datetime":
                property_str = self.build_datetime_property(field_name, field_desc)
            else:
                constraints = {k: v for k, v in field_data[1].items() 
                             if k not in ('type', 'desc')}
                
                property_info = PropertyInfo(
                    name=field_name,
                    type=field_type,
                    description=field_desc,
                    constraints=constraints,
                    is_optional=constraints.get('option', False)
                )
                property_str = self.build_typed_property(property_info)
            
            properties.append(property_str)
        
        return properties
    
    def extract_required_fields(self, fields: Dict[str, Any]) -> List[str]:
        """필수 필드들을 추출.
        
        Args:
            fields: 필드 정보 딕셔너리
            
        Returns:
            필수 필드명 리스트
        """
        required_fields = []
        
        for field_key, field_value in fields.items():
            field_data = field_value[-1]
            field_elements = field_key.split('.')
            field_name = field_elements[-1]
            
            # option이 False이거나 없으면 필수 필드
            is_optional = field_data[1].get('option', False)
            if not is_optional:
                required_fields.append(field_name)
        
        return required_fields