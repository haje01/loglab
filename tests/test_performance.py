"""성능 테스트."""

import json
import os
import tempfile
import time
from unittest.mock import patch

import psutil
import pytest
from click.testing import CliRunner

from loglab.cli import cli
from loglab.model import build_model
from loglab.schema.generator import LogSchemaGenerator


class TestPerformance:
    """성능 테스트 클래스."""

    @pytest.fixture
    def large_lab_data(self):
        """대용량 lab 데이터 생성."""
        lab_data = {
            "domain": {
                "name": "performance_test",
                "desc": "성능 테스트용 대용량 도메인",
            },
            "types": {},
            "bases": {},
            "events": {},
        }

        # 대량의 커스텀 타입 생성
        for i in range(50):
            lab_data["types"][f"CustomType{i}"] = {
                "type": "integer",
                "desc": f"커스텀 타입 {i}",
                "minimum": 0,
                "maximum": 1000,
            }

        # 대량의 베이스 생성
        for i in range(20):
            lab_data["bases"][f"Base{i}"] = {
                "desc": f"베이스 클래스 {i}",
                "fields": [
                    [f"Field{j}", f"types.CustomType{j % 50}", f"필드 {j}"]
                    for j in range(10)
                ],
            }

        # 대량의 이벤트 생성
        for i in range(200):
            event_fields = [
                ["DateTime", "datetime", "이벤트 일시"],
                ["EventId", "integer", "이벤트 ID"],
                ["UserId", f"types.CustomType{i % 50}", "사용자 ID"],
            ]

            # 일부 이벤트에 베이스 믹스인 추가
            mixins = []
            if i % 10 == 0:
                mixins.append(f"bases.Base{i % 20}")

            # 추가 필드
            for j in range(15):
                event_fields.append(
                    [
                        f"Field{j}",
                        ["string", "integer", "number", "boolean"][j % 4],
                        f"필드 {j} 설명",
                    ]
                )

            lab_data["events"][f"Event{i}"] = {
                "desc": f"이벤트 {i} 설명",
                "fields": event_fields,
            }

            if mixins:
                lab_data["events"][f"Event{i}"]["mixins"] = mixins

        return lab_data

    def test_model_build_performance(self, large_lab_data):
        """모델 빌드 성능 테스트."""
        start_time = time.time()

        model = build_model(large_lab_data)

        end_time = time.time()
        build_time = end_time - start_time

        # 5초 이내에 빌드되어야 함
        assert build_time < 5.0, f"Model build took {build_time:.2f}s, expected < 5.0s"

        # 모델이 올바르게 생성되었는지 확인
        assert hasattr(model, "domain")
        assert hasattr(model, "events")
        assert len(model.events) == 200

    def test_schema_generation_performance(self, large_lab_data):
        """스키마 생성 성능 테스트."""
        generator = LogSchemaGenerator()

        start_time = time.time()

        schema = generator.generate_schema(large_lab_data)

        end_time = time.time()
        generation_time = end_time - start_time

        # 10초 이내에 생성되어야 함
        assert (
            generation_time < 10.0
        ), f"Schema generation took {generation_time:.2f}s, expected < 10.0s"

        # 스키마가 올바르게 생성되었는지 확인
        assert isinstance(schema, str)
        assert "performance_test" in schema
        assert "$defs" in schema

    def test_memory_usage(self, large_lab_data):
        """메모리 사용량 테스트."""
        process = psutil.Process()

        # 초기 메모리 사용량
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # 모델 빌드
        model = build_model(large_lab_data)

        # 스키마 생성
        generator = LogSchemaGenerator()
        schema = generator.generate_schema(large_lab_data)

        # 최종 메모리 사용량
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # 메모리 증가량이 100MB 이하여야 함
        assert (
            memory_increase < 100
        ), f"Memory increase: {memory_increase:.2f}MB, expected < 100MB"

    def test_cli_performance(self, large_lab_data):
        """CLI 성능 테스트."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".lab.json"
        ) as f:
            json.dump(large_lab_data, f, ensure_ascii=False)
            lab_path = f.name

        runner = CliRunner()

        try:
            # show 명령 성능
            start_time = time.time()
            result = runner.invoke(cli, ["show", lab_path])
            show_time = time.time() - start_time

            assert result.exit_code == 0
            assert show_time < 3.0, f"CLI show took {show_time:.2f}s, expected < 3.0s"

            # schema 명령 성능
            start_time = time.time()
            result = runner.invoke(cli, ["schema", lab_path])
            schema_time = time.time() - start_time

            assert result.exit_code == 0
            assert (
                schema_time < 8.0
            ), f"CLI schema took {schema_time:.2f}s, expected < 8.0s"

        finally:
            os.unlink(lab_path)
            # 생성된 스키마 파일 정리
            schema_file = lab_path.replace(".lab.json", ".schema.json")
            if os.path.exists(schema_file):
                os.unlink(schema_file)


class TestScalability:
    """확장성 테스트."""

    @pytest.mark.parametrize("event_count", [10, 50, 100, 500])
    def test_scaling_with_event_count(self, event_count):
        """이벤트 수에 따른 확장성 테스트."""
        lab_data = {
            "domain": {
                "name": f"scale_test_{event_count}",
                "desc": f"{event_count}개 이벤트 확장성 테스트",
            },
            "events": {},
        }

        # 지정된 수만큼 이벤트 생성
        for i in range(event_count):
            lab_data["events"][f"Event{i}"] = {
                "desc": f"이벤트 {i}",
                "fields": [
                    ["DateTime", "datetime", "이벤트 일시"],
                    ["EventId", "integer", "이벤트 ID"],
                    ["Data", "string", "데이터"],
                ],
            }

        start_time = time.time()
        model = build_model(lab_data)
        build_time = time.time() - start_time

        # 빌드 시간이 이벤트 수에 비례해서 선형적으로 증가하는지 확인
        # 대략 이벤트당 0.01초 이하여야 함
        expected_max_time = event_count * 0.01 + 1.0  # 기본 오버헤드 1초
        assert (
            build_time < expected_max_time
        ), f"Build time {build_time:.2f}s exceeded expected {expected_max_time:.2f}s for {event_count} events"

        assert len(model.events) == event_count

    def test_deep_inheritance_performance(self):
        """깊은 상속 구조 성능 테스트."""
        lab_data = {
            "domain": {
                "name": "deep_inheritance_test",
                "desc": "깊은 상속 구조 테스트",
            },
            "bases": {},
            "events": {},
        }

        # 깊은 상속 체인 생성 (10단계)
        for i in range(10):
            mixins = []
            if i > 0:
                mixins.append(f"bases.Base{i-1}")

            lab_data["bases"][f"Base{i}"] = {
                "desc": f"베이스 {i}",
                "fields": [[f"Field{i}", "string", f"필드 {i}"]],
            }

            if mixins:
                lab_data["bases"][f"Base{i}"]["mixins"] = mixins

        # 최종 베이스를 사용하는 이벤트
        lab_data["events"]["DeepEvent"] = {
            "desc": "깊은 상속 이벤트",
            "mixins": ["bases.Base9"],
            "fields": [["EventData", "string", "이벤트 데이터"]],
        }

        start_time = time.time()
        model = build_model(lab_data)
        build_time = time.time() - start_time

        # 복잡한 상속 구조도 합리적인 시간 내에 처리되어야 함
        assert (
            build_time < 2.0
        ), f"Deep inheritance build took {build_time:.2f}s, expected < 2.0s"

        # 모든 필드가 올바르게 상속되었는지 확인
        deep_event_fields = model.events["DeepEvent"][-1][1]["fields"]
        assert len(deep_event_fields) >= 10  # DateTime + EventData + 상속받은 필드들
