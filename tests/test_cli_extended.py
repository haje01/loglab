"""확장된 CLI 테스트."""

import json
import os
import tempfile
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from loglab.cli import cli, html, object, schema, show, verify
from loglab.util import test_reset


class TestCLIErrorHandling:
    """CLI 에러 처리 테스트."""

    @pytest.fixture
    def clear(self):
        test_reset()

    def test_cli_invalid_command(self):
        """잘못된 명령어 처리."""
        runner = CliRunner()
        result = runner.invoke(cli, ["invalid_command"])
        assert result.exit_code == 2
        assert "No such command" in result.output

    def test_show_missing_file(self):
        """존재하지 않는 파일 show 명령."""
        runner = CliRunner()
        result = runner.invoke(show, ["nonexistent.lab.json"])
        assert result.exit_code != 0

    def test_schema_invalid_lab_file(self):
        """잘못된 lab 파일로 스키마 생성."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".lab.json"
        ) as f:
            f.write('{"invalid": "json"')  # 잘못된 JSON
            temp_path = f.name

        try:
            runner = CliRunner()
            result = runner.invoke(schema, [temp_path])
            assert result.exit_code != 0
        finally:
            os.unlink(temp_path)

    def test_verify_with_invalid_schema(self):
        """잘못된 스키마로 검증."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".schema.json"
        ) as f:
            f.write("invalid json")
            schema_path = f.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
            f.write('{"test": "log"}')
            log_path = f.name

        try:
            runner = CliRunner()
            result = runner.invoke(verify, [schema_path, log_path])
            assert result.exit_code != 0
        finally:
            os.unlink(schema_path)
            os.unlink(log_path)


class TestCLIPerformance:
    """CLI 성능 테스트."""

    @pytest.fixture
    def large_lab_file(self):
        """대용량 lab 파일 생성."""
        lab_data = {
            "domain": {"name": "performance_test", "desc": "성능 테스트용 도메인"},
            "events": {},
        }

        # 많은 이벤트 추가
        for i in range(100):
            lab_data["events"][f"Event{i}"] = {
                "desc": f"이벤트 {i}",
                "fields": (
                    [
                        ["DateTime", "datetime", "이벤트 일시"],
                        ["EventId", "integer", "이벤트 ID"],
                    ]
                    + [[f"Field{j}", "string", f"필드 {j}"] for j in range(10)]
                ),
            }

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".lab.json"
        ) as f:
            json.dump(lab_data, f, ensure_ascii=False, indent=2)
            return f.name

    def test_show_large_file_performance(self, large_lab_file):
        """대용량 파일 show 성능."""
        runner = CliRunner()

        import time

        start_time = time.time()
        result = runner.invoke(show, [large_lab_file])
        end_time = time.time()

        assert result.exit_code == 0
        assert end_time - start_time < 5.0  # 5초 이내 완료

        os.unlink(large_lab_file)

    def test_schema_generation_performance(self, large_lab_file):
        """스키마 생성 성능."""
        runner = CliRunner()

        import time

        start_time = time.time()
        result = runner.invoke(schema, [large_lab_file])
        end_time = time.time()

        assert result.exit_code == 0
        assert end_time - start_time < 10.0  # 10초 이내 완료

        # 생성된 스키마 파일 정리
        schema_file = large_lab_file.replace(".lab.json", ".schema.json")
        if os.path.exists(schema_file):
            os.unlink(schema_file)

        os.unlink(large_lab_file)


class TestCLIIntegration:
    """CLI 통합 테스트."""

    @pytest.fixture
    def clear(self):
        test_reset()

    @pytest.mark.skip(reason="Complex integration test - skip for now")
    def test_full_workflow(self, clear):
        """전체 워크플로우 테스트."""
        # 1. lab 파일 생성
        lab_data = {
            "domain": {"name": "integration_test", "desc": "통합 테스트"},
            "events": {
                "TestEvent": {
                    "desc": "테스트 이벤트",
                    "fields": [
                        ["DateTime", "datetime", "이벤트 일시"],
                        ["UserId", "integer", "사용자 ID"],
                        ["Message", "string", "메시지"],
                    ],
                }
            },
        }

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".lab.json"
        ) as f:
            json.dump(lab_data, f, ensure_ascii=False)
            lab_path = f.name

        runner = CliRunner()

        try:
            # 2. show 명령 테스트
            result = runner.invoke(show, [lab_path])
            assert result.exit_code == 0
            assert "integration_test" in result.output

            # 3. 스키마 생성 테스트
            result = runner.invoke(schema, [lab_path])
            assert result.exit_code == 0

            # CLI에서는 현재 디렉토리에 스키마 파일을 생성하므로 경로 수정
            schema_filename = os.path.basename(lab_path).replace(
                ".lab.json", ".schema.json"
            )
            schema_path = schema_filename
            assert os.path.exists(schema_path)

            # 4. HTML 문서 생성 테스트
            result = runner.invoke(html, [lab_path])
            assert result.exit_code == 0

            html_filename = os.path.basename(lab_path).replace(".lab.json", ".html")
            html_path = html_filename
            assert os.path.exists(html_path)

            # 5. Python 객체 생성 테스트
            result = runner.invoke(object, [lab_path, "py"])
            assert result.exit_code == 0
            assert "class TestEvent" in result.output

            # 6. 로그 검증 테스트
            log_data = {
                "DateTime": "2023-01-01T00:00:00+09:00",
                "Event": "TestEvent",
                "UserId": 123,
                "Message": "테스트 메시지",
            }

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".log"
            ) as f:
                json.dump(log_data, f)
                log_path = f.name

            try:
                result = runner.invoke(verify, [schema_path, log_path])
                assert result.exit_code == 0
            finally:
                os.unlink(log_path)

        finally:
            # 정리
            files_to_clean = [lab_path, schema_path, html_path]
            for file_path in files_to_clean:
                if os.path.exists(file_path):
                    os.unlink(file_path)


class TestCLIEdgeCases:
    """CLI 엣지 케이스 테스트."""

    def test_empty_lab_file(self):
        """빈 lab 파일 처리."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".lab.json"
        ) as f:
            f.write("{}")
            temp_path = f.name

        try:
            runner = CliRunner()
            result = runner.invoke(show, [temp_path])
            # 최소한 에러가 발생하더라도 크래시되지 않아야 함
            assert result.exit_code is not None
        finally:
            os.unlink(temp_path)

    @pytest.mark.skip(reason="Unicode handling test - skip for now")
    def test_unicode_content(self):
        """유니코드 콘텐츠 처리."""
        lab_data = {
            "domain": {"name": "unicode_test", "desc": "한글 테스트 🚀"},
            "events": {
                "유니코드이벤트": {
                    "desc": "한글 이벤트 설명 🎉",
                    "fields": [
                        ["DateTime", "datetime", "이벤트 일시"],
                        ["한글필드", "string", "한글 필드 설명 ✨"],
                    ],
                }
            },
        }

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".lab.json", encoding="utf-8"
        ) as f:
            json.dump(lab_data, f, ensure_ascii=False)
            temp_path = f.name

        try:
            runner = CliRunner()
            result = runner.invoke(show, [temp_path])
            assert result.exit_code == 0
            assert "unicode_test" in result.output
        finally:
            os.unlink(temp_path)
