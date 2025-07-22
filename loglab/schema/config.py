"""Schema 관련 설정."""

import dataclasses
import os

from loglab.util import LOGLAB_HOME


@dataclasses.dataclass
class SchemaConfig:
    """스키마 검증 및 생성 관련 설정."""

    default_schema_path: str = dataclasses.field(
        default_factory=lambda: os.path.join(LOGLAB_HOME, "schema", "lab.schema.json")
    )

    datetime_pattern: str = (
        r"^([0-9]+)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])[Tt]"
        r"([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]|60)"
        r"(\\\\.[0-9]+)?(([Zz])|([\\\\+|\\\\-]([01][0-9]|2[0-3]):?[0-5][0-9]))$"
    )

    json_schema_version: str = "https://json-schema.org/draft/2020-12/schema"

    encoding: str = "utf8"
