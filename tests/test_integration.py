"""통합 테스트."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from loglab.cli import cli
from loglab.doc import html_from_labfile
from loglab.model import build_model
from loglab.schema.generator import LogSchemaGenerator
from loglab.schema.log_validator import LogFileValidator


class TestEndToEndWorkflow:
    """전체 워크플로우 통합 테스트."""

    @pytest.fixture
    def sample_lab_data(self):
        """샘플 lab 데이터."""
        return {
            "domain": {"name": "integration_test", "desc": "통합 테스트 도메인"},
            "types": {
                "UserId": {"type": "integer", "desc": "사용자 ID 타입", "minimum": 1}
            },
            "bases": {
                "UserInfo": {
                    "desc": "사용자 정보",
                    "fields": [
                        ["UserId", "types.UserId", "사용자 ID"],
                        ["UserName", "string", "사용자 이름"],
                    ],
                },
                "ServerInfo": {
                    "desc": "서버 정보",
                    "fields": [["ServerNo", "integer", "서버 번호"]],
                },
            },
            "events": {
                "Login": {
                    "desc": "로그인 이벤트",
                    "mixins": ["bases.UserInfo", "bases.ServerInfo"],
                    "fields": [
                        [
                            "Platform",
                            "string",
                            "플랫폼",
                            False,
                            ["ios", "android", "web"],
                        ]
                    ],
                },
                "Logout": {
                    "desc": "로그아웃 이벤트",
                    "mixins": ["bases.UserInfo"],
                    "fields": [["Duration", "number", "접속 시간 (초)", True]],
                },
            },
        }

    @pytest.mark.skip(reason="Complex integration workflow - skip for now")
    def test_complete_workflow(self, sample_lab_data):
        """완전한 워크플로우 테스트."""
        with tempfile.TemporaryDirectory() as temp_dir:
            lab_path = os.path.join(temp_dir, "test.lab.json")

            # 1. Lab 파일 작성
            with open(lab_path, "w", encoding="utf-8") as f:
                json.dump(sample_lab_data, f, ensure_ascii=False, indent=2)

            # 2. 모델 빌드
            model = build_model(sample_lab_data)
            assert model.domain.name == "integration_test"
            assert "Login" in model.events
            assert "Logout" in model.events

            # 3. 스키마 생성
            generator = LogSchemaGenerator()
            schema_json = generator.generate_schema(sample_lab_data)
            assert isinstance(schema_json, str)

            schema_path = os.path.join(temp_dir, "test.schema.json")
            with open(schema_path, "w", encoding="utf-8") as f:
                f.write(schema_json)

            # 4. HTML 문서 생성
            html_content = html_from_labfile(sample_lab_data, {}, False, None)
            assert "integration_test" in html_content
            assert "Login" in html_content

            # 5. 로그 데이터 생성 및 검증
            valid_logs = [
                {
                    "DateTime": "2023-01-01T10:00:00+09:00",
                    "Event": "Login",
                    "UserId": 123,
                    "UserName": "testuser",
                    "ServerNo": 1,
                    "Platform": "ios",
                },
                {
                    "DateTime": "2023-01-01T10:30:00+09:00",
                    "Event": "Logout",
                    "UserId": 123,
                    "UserName": "testuser",
                    "Duration": 1800.5,
                },
            ]

            log_path = os.path.join(temp_dir, "test.log")
            with open(log_path, "w", encoding="utf-8") as f:
                for log in valid_logs:
                    f.write(json.dumps(log, ensure_ascii=False) + "\n")

            # 6. 로그 검증
            validator = LogFileValidator()
            result = validator.validate_log_file(schema_path, log_path)
            assert result.success is True

            # 7. 잘못된 로그 검증
            invalid_log = {
                "DateTime": "2023-01-01T10:00:00+09:00",
                "Event": "Login",
                "UserId": "invalid",  # 문자열이지만 숫자여야 함
                "UserName": "testuser",
                "ServerNo": 1,
                "Platform": "invalid_platform",  # 허용되지 않는 값
            }

            invalid_log_path = os.path.join(temp_dir, "invalid.log")
            with open(invalid_log_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(invalid_log, ensure_ascii=False))

            result = validator.validate_log_file(schema_path, invalid_log_path)
            assert result.success is False
            assert len(result.errors) > 0

    @pytest.mark.skip(reason="CLI integration test - skip for now")
    def test_cli_integration(self, sample_lab_data):
        """CLI 통합 테스트."""
        with tempfile.TemporaryDirectory() as temp_dir:
            lab_path = os.path.join(temp_dir, "cli_test.lab.json")

            # Lab 파일 작성
            with open(lab_path, "w", encoding="utf-8") as f:
                json.dump(sample_lab_data, f, ensure_ascii=False, indent=2)

            runner = CliRunner()

            # show 명령
            result = runner.invoke(cli, ["show", lab_path])
            assert result.exit_code == 0
            assert "integration_test" in result.output
            assert "Login" in result.output

            # schema 명령
            result = runner.invoke(cli, ["schema", lab_path])
            assert result.exit_code == 0

            schema_path = lab_path.replace(".lab.json", ".schema.json")
            assert os.path.exists(schema_path)

            # html 명령
            result = runner.invoke(cli, ["html", lab_path])
            assert result.exit_code == 0

            html_path = lab_path.replace(".lab.json", ".html")
            assert os.path.exists(html_path)

            # 생성된 HTML 내용 확인
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
                assert "integration_test" in html_content
                assert "Login" in html_content

            # object 명령 (Python)
            result = runner.invoke(cli, ["object", lab_path, "py"])
            assert result.exit_code == 0
            assert "class Login" in result.output
            assert "class Logout" in result.output


class TestMultiLanguageCodeGeneration:
    """다언어 코드 생성 통합 테스트."""

    @pytest.fixture
    def code_gen_lab_data(self):
        """코드 생성용 lab 데이터."""
        return {
            "domain": {"name": "codegen_test", "desc": "코드 생성 테스트"},
            "events": {
                "SimpleEvent": {
                    "desc": "간단한 이벤트",
                    "fields": [
                        ["EventId", "integer", "이벤트 ID"],
                        ["Message", "string", "메시지"],
                    ],
                }
            },
        }

    @pytest.mark.skip(reason="Python code generation test - skip for now")
    def test_python_code_generation(self, code_gen_lab_data):
        """Python 코드 생성 테스트."""
        with tempfile.TemporaryDirectory() as temp_dir:
            lab_path = os.path.join(temp_dir, "codegen.lab.json")

            with open(lab_path, "w", encoding="utf-8") as f:
                json.dump(code_gen_lab_data, f, ensure_ascii=False)

            runner = CliRunner()

            # Python 코드 생성
            py_output_path = os.path.join(temp_dir, "test_objects.py")
            result = runner.invoke(
                cli, ["object", lab_path, "py", "-o", py_output_path]
            )
            assert result.exit_code == 0
            assert os.path.exists(py_output_path)

            # 생성된 Python 코드 검증
            with open(py_output_path, "r", encoding="utf-8") as f:
                code = f.read()
                assert "class SimpleEvent" in code
                assert "def __init__" in code
                assert "def serialize" in code

            # Python 코드 실행 테스트
            try:
                # 생성된 코드를 임포트해서 실행
                import sys

                sys.path.insert(0, temp_dir)

                # 동적 임포트
                import importlib.util

                spec = importlib.util.spec_from_file_location(
                    "test_objects", py_output_path
                )
                test_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(test_module)

                # 객체 생성 및 직렬화 테스트
                event = test_module.SimpleEvent(123, "테스트 메시지")
                serialized = event.serialize()

                # JSON 파싱 확인
                import json

                data = json.loads(serialized)
                assert data["Event"] == "SimpleEvent"
                assert data["EventId"] == 123
                assert data["Message"] == "테스트 메시지"

            except Exception as e:
                pytest.fail(f"Generated Python code execution failed: {e}")

    @pytest.mark.skipif(not shutil.which("dotnet"), reason="dotnet not available")
    def test_csharp_code_generation(self, code_gen_lab_data):
        """C# 코드 생성 테스트 (dotnet 설치된 경우만)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            lab_path = os.path.join(temp_dir, "codegen.lab.json")

            with open(lab_path, "w", encoding="utf-8") as f:
                json.dump(code_gen_lab_data, f, ensure_ascii=False)

            runner = CliRunner()

            # C# 코드 생성
            cs_output_path = os.path.join(temp_dir, "TestObjects.cs")
            result = runner.invoke(
                cli, ["object", lab_path, "cs", "-o", cs_output_path]
            )
            assert result.exit_code == 0
            assert os.path.exists(cs_output_path)

            # 생성된 C# 코드 검증
            with open(cs_output_path, "r", encoding="utf-8") as f:
                code = f.read()
                assert "public class SimpleEvent" in code
                assert "public string Serialize()" in code

    @pytest.mark.skipif(not shutil.which("g++"), reason="g++ not available")
    def test_cpp_code_generation(self, code_gen_lab_data):
        """C++ 코드 생성 테스트 (g++ 설치된 경우만)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            lab_path = os.path.join(temp_dir, "codegen.lab.json")

            with open(lab_path, "w", encoding="utf-8") as f:
                json.dump(code_gen_lab_data, f, ensure_ascii=False)

            runner = CliRunner()

            # C++ 코드 생성
            cpp_output_path = os.path.join(temp_dir, "test_objects.h")
            result = runner.invoke(
                cli, ["object", lab_path, "cpp", "-o", cpp_output_path]
            )
            assert result.exit_code == 0
            assert os.path.exists(cpp_output_path)

            # 생성된 C++ 코드 검증
            with open(cpp_output_path, "r", encoding="utf-8") as f:
                code = f.read()
                assert "class SimpleEvent" in code
                assert "serialize()" in code  # C++ 템플릿에서는 std::string&를 반환


class TestErrorRecovery:
    """에러 복구 통합 테스트."""

    def test_invalid_lab_file_recovery(self):
        """잘못된 lab 파일에서 복구."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 잘못된 JSON 파일
            invalid_lab_path = os.path.join(temp_dir, "invalid.lab.json")
            with open(invalid_lab_path, "w") as f:
                f.write('{"invalid": json}')  # 문법 오류

            runner = CliRunner()
            result = runner.invoke(cli, ["show", invalid_lab_path])

            # 크래시되지 않고 적절한 에러 메시지를 반환해야 함
            assert result.exit_code != 0
            assert result.output is not None

    def test_missing_dependencies_recovery(self):
        """의존성 누락 시 복구."""
        lab_data = {
            "domain": {"name": "dependency_test", "desc": "의존성 테스트"},
            "events": {
                "TestEvent": {
                    "desc": "테스트 이벤트",
                    "mixins": ["bases.NonExistent"],  # 존재하지 않는 베이스
                    "fields": [
                        [
                            "Field1",
                            "types.NonExistent",
                            "존재하지 않는 타입",
                        ]  # 존재하지 않는 타입
                    ],
                }
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            lab_path = os.path.join(temp_dir, "dependency.lab.json")
            with open(lab_path, "w", encoding="utf-8") as f:
                json.dump(lab_data, f, ensure_ascii=False)

            runner = CliRunner()
            result = runner.invoke(cli, ["show", lab_path])

            # 적절한 에러 처리가 되어야 함
            assert result.exit_code != 0
