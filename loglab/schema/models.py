"""Schema 생성에 필요한 모델 클래스들."""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class EventSchema:
    """이벤트 스키마 정보."""
    name: str
    properties: List[str]  # 문자열 리스트로 변경 (기존 방식과 호환)
    required_fields: List[str]
    description: str = ""


@dataclass
class PropertyInfo:
    """필드 속성 정보."""
    name: str
    type: str
    description: str
    constraints: Dict[str, Any]
    is_optional: bool = False


@dataclass
class DomainInfo:
    """도메인 정보."""
    name: str
    description: str