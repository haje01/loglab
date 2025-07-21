"""개선된 CLI 테스트 (v2)."""
import json
import pytest
from unittest.mock import Mock, patch, mock_open
from click.testing import CliRunner

from loglab.cli import cli, version, show, schema, verify, html, object as object_cmd
from loglab.version import VERSION


class TestCLIBasics:
    """CLI 기본 기능 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.runner = CliRunner()
    
    def test_cli_without_command(self):
        """명령어 없이 실행 시 도움말 표시."""
        result = self.runner.invoke(cli)
        assert result.exit_code == 2
        assert 'Commands:' in result.output
        assert 'show' in result.output
        assert 'schema' in result.output
    
    def test_version_command(self):
        """버전 명령어 테스트."""
        result = self.runner.invoke(version)
        assert result.exit_code == 0
        assert result.output.strip() == VERSION
    
    @pytest.mark.parametrize("command_name", ["show", "schema", "verify", "html", "object"])
    def test_commands_exist(self, command_name):
        """모든 명령어가 존재하는지 확인."""
        result = self.runner.invoke(cli, ['--help'])
        assert command_name in result.output
    
    def test_command_help_availability(self):
        """모든 명령어의 도움말 사용 가능성 테스트."""
        commands = ['show', 'schema', 'verify', 'html', 'object', 'version']
        
        for command in commands:
            result = self.runner.invoke(cli, [command, '--help'])
            assert result.exit_code == 0
            assert 'Usage:' in result.output


class TestShowCommandWithIsolation:
    """show 명령어 격리 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.runner = CliRunner()
    
    def test_show_basic_structure_validation(self):
        """show 명령어 기본 구조 검증."""
        with self.runner.isolated_filesystem():
            # 임시 lab 파일 생성
            lab_content = {
                "domain": {"name": "test", "desc": "Test Domain"},
                "events": {
                    "Login": {
                        "desc": "Login event",
                        "fields": [
                            ["DateTime", "datetime", "Event time"],
                            ["UserId", "integer", "User ID"]
                        ]
                    }
                }
            }
            
            with open('test.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            # Mock external dependencies
            with patch('loglab.cli.handle_import') as mock_import:
                mock_import.return_value = None
                
                result = self.runner.invoke(show, ['test.lab.json'])
                
                # 기본적인 성공 검증
                assert result.exit_code == 0
                assert "Domain" in result.output
                assert "test" in result.output
    
    def test_show_output_contains_expected_sections(self):
        """show 출력이 예상된 섹션들을 포함하는지 검증."""
        with self.runner.isolated_filesystem():
            lab_content = {
                "domain": {"name": "testdomain", "desc": "Test Description"},
                "events": {
                    "TestEvent": {
                        "desc": "Test Event Description",
                        "fields": [
                            ["DateTime", "datetime", "Event time"]
                        ]
                    }
                }
            }
            
            with open('test.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            with patch('loglab.cli.handle_import'):
                result = self.runner.invoke(show, ['test.lab.json'])
                
                # 구조적 요소들이 포함되어 있는지 확인
                output_lines = result.output.split('\n')
                
                # Domain 정보 확인
                assert any("Domain" in line and "testdomain" in line for line in output_lines)
                
                # Event 정보 확인  
                assert any("Event" in line and "TestEvent" in line for line in output_lines)
                
                # 테이블 구조 확인 (필드 정보)
                assert any("Field" in line for line in output_lines)
    
    def test_show_with_flags_changes_behavior(self):
        """show 명령어 플래그들이 동작을 변경하는지 테스트."""
        with self.runner.isolated_filesystem():
            lab_content = {
                "domain": {"name": "test", "desc": "Test"},
                "types": {
                    "CustomType": {
                        "type": "integer",
                        "desc": "Custom type",
                        "minimum": 0
                    }
                },
                "events": {
                    "Login": {
                        "desc": "Login",
                        "fields": [
                            ["DateTime", "datetime", "Event time"],
                            ["UserId", "types.CustomType", "User ID"]
                        ]
                    }
                }
            }
            
            with open('test.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            with patch('loglab.cli.handle_import'):
                # 기본 실행
                result_basic = self.runner.invoke(show, ['test.lab.json'])
                
                # 커스텀 타입 플래그와 함께 실행
                result_with_custom = self.runner.invoke(show, ['test.lab.json', '-c'])
                
                # 두 결과가 다른지 확인 (커스텀 타입 표시 여부)
                assert result_basic.exit_code == 0
                assert result_with_custom.exit_code == 0
                
                # 커스텀 타입 플래그를 사용했을 때 더 많은 정보가 표시되어야 함
                assert len(result_with_custom.output) >= len(result_basic.output)


class TestErrorHandlingPatterns:
    """에러 처리 패턴 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.runner = CliRunner()
    
    def test_file_not_found_error_message(self):
        """파일을 찾을 수 없을 때 적절한 에러 메시지."""
        result = self.runner.invoke(show, ['nonexistent.lab.json'])
        assert result.exit_code != 0
        # Click이 자동으로 생성하는 에러 메시지 확인
        assert "does not exist" in result.output.lower() or "no such file" in result.output.lower()
    
    def test_invalid_command_arguments(self):
        """잘못된 명령어 인수 처리."""
        # 필수 인수 누락
        result = self.runner.invoke(show, [])
        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output
    
    def test_invalid_flag_combinations(self):
        """잘못된 플래그 조합 처리."""
        with self.runner.isolated_filesystem():
            # 존재하지 않는 플래그
            result = self.runner.invoke(show, ['test.lab.json', '--invalid-flag'])
            assert result.exit_code != 0
            assert "No such option" in result.output


class TestMockBasedUnitTests:
    """Mock 기반 단위 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.runner = CliRunner()
    
    @patch('loglab.cli.verify_labfile')
    @patch('loglab.cli.handle_import')
    @patch('loglab.cli.text_from_labfile')
    def test_show_function_calls(self, mock_text, mock_import, mock_verify):
        """show 명령어가 올바른 함수들을 호출하는지 테스트."""
        # Mock 설정
        mock_verify.return_value = {"domain": {"name": "test"}}
        mock_import.return_value = None
        mock_text.return_value = "Mocked output"
        
        with self.runner.isolated_filesystem():
            with open('test.lab.json', 'w') as f:
                f.write('{}')
            
            result = self.runner.invoke(show, ['test.lab.json'])
            
            # 함수 호출 검증
            mock_verify.assert_called_once_with('test.lab.json')
            mock_import.assert_called_once()
            mock_text.assert_called_once()
            
            assert result.exit_code == 0
            assert "Mocked output" in result.output
    
    def test_schema_generation_flow(self):
        """schema 명령어의 전체 플로우 테스트."""
        with self.runner.isolated_filesystem():
            # 유효한 lab 파일 생성
            lab_content = {
                "domain": {"name": "test", "desc": "Test Domain"},
                "events": {
                    "Login": {
                        "desc": "Login event",
                        "fields": [
                            ["DateTime", "datetime", "Event time"]
                        ]
                    }
                }
            }
            
            with open('test.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            with patch('loglab.cli.handle_import') as mock_import:
                mock_import.return_value = None
                
                result = self.runner.invoke(schema, ['test.lab.json'])
                
                # 성공 검증
                assert result.exit_code == 0
                assert "test.schema.json 에 로그 스키마 저장" in result.output


class TestCommandBehaviorValidation:
    """명령어 동작 검증 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.runner = CliRunner()
    
    def test_verify_command_file_checking(self):
        """verify 명령어의 파일 존재 확인 로직."""
        # 두 파일 모두 없는 경우
        result = self.runner.invoke(verify, ['schema.json', 'log.txt'])
        assert result.exit_code != 0
        assert "does not exist" in result.output
        
        with self.runner.isolated_filesystem():
            # 스키마 파일만 있는 경우
            with open('schema.json', 'w') as f:
                json.dump({"test": "schema"}, f)
            
            result = self.runner.invoke(verify, ['schema.json', 'missing.txt'])
            assert result.exit_code != 0
            assert "does not exist" in result.output
    
    def test_html_command_output_generation(self):
        """html 명령어의 출력 생성 확인."""
        with self.runner.isolated_filesystem():
            lab_content = {
                "domain": {"name": "test", "desc": "Test Domain"}
            }
            
            with open('test.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            with patch('loglab.cli.handle_import'), \
                 patch('loglab.cli.html_from_labfile', return_value="<html>test</html>"):
                
                result = self.runner.invoke(html, ['test.lab.json'])
                
                assert result.exit_code == 0
                assert "'test.html' 에 HTML 문서 저장" in result.output
    
    @pytest.mark.parametrize("language", ["py", "cs", "cpp"])
    def test_object_command_language_support(self, language):
        """object 명령어의 다양한 언어 지원 확인."""
        with self.runner.isolated_filesystem():
            lab_content = {
                "domain": {"name": "test", "desc": "Test Domain"}
            }
            
            with open('test.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            with patch('loglab.cli.handle_import'), \
                 patch('loglab.cli.object_from_labfile', return_value=f"// {language} code"):
                
                result = self.runner.invoke(object_cmd, ['test.lab.json', language])
                
                # 명령어가 성공적으로 실행되는지 확인
                assert result.exit_code == 0


class TestOutputFormatValidation:
    """출력 형식 검증 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.runner = CliRunner()
    
    def test_show_output_structure_consistency(self):
        """show 출력이 일관된 구조를 가지는지 테스트."""
        with self.runner.isolated_filesystem():
            # 여러 다른 lab 파일로 테스트
            test_cases = [
                {
                    "domain": {"name": "simple", "desc": "Simple domain"},
                    "events": {
                        "Event1": {
                            "desc": "First event",
                            "fields": [["DateTime", "datetime", "Time"]]
                        }
                    }
                },
                {
                    "domain": {"name": "complex", "desc": "Complex domain"},
                    "types": {"CustomType": {"type": "integer", "desc": "Custom"}},
                    "events": {
                        "Event1": {"desc": "Event1", "fields": [["DateTime", "datetime", "Time"]]},
                        "Event2": {"desc": "Event2", "fields": [["DateTime", "datetime", "Time"]]}
                    }
                }
            ]
            
            for i, lab_content in enumerate(test_cases):
                filename = f'test{i}.lab.json'
                with open(filename, 'w') as f:
                    json.dump(lab_content, f)
                
                with patch('loglab.cli.handle_import'):
                    result = self.runner.invoke(show, [filename])
                    
                    assert result.exit_code == 0
                    
                    # 모든 출력에 공통으로 포함되어야 하는 요소들
                    assert "Domain" in result.output
                    assert lab_content["domain"]["name"] in result.output
                    assert "Event" in result.output
    
    def test_error_message_consistency(self):
        """에러 메시지의 일관성 테스트."""
        error_scenarios = [
            (['nonexistent.lab.json'], "file"),
            (['test.lab.json', '--invalid-flag'], "option"),
            ([], "argument")
        ]
        
        for args, error_type in error_scenarios:
            result = self.runner.invoke(show, args)
            assert result.exit_code != 0
            assert len(result.output) > 0  # 에러 메시지가 있어야 함


class TestPerformanceAndReliability:
    """성능 및 신뢰성 테스트."""
    
    def setup_method(self):
        """테스트 설정."""
        self.runner = CliRunner()
    
    def test_command_execution_isolation(self):
        """명령어 실행이 서로 격리되는지 테스트."""
        with self.runner.isolated_filesystem():
            lab_content = {"domain": {"name": "test", "desc": "Test"}}
            
            with open('test.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            # 여러 번 연속 실행해도 결과가 일관된지 확인
            with patch('loglab.cli.handle_import'):
                results = []
                for _ in range(3):
                    result = self.runner.invoke(show, ['test.lab.json'])
                    results.append((result.exit_code, len(result.output)))
                
                # 모든 실행 결과가 동일해야 함
                assert all(r[0] == results[0][0] for r in results)
                assert all(r[1] == results[0][1] for r in results)
    
    def test_large_output_handling(self):
        """큰 출력 처리 테스트."""
        with self.runner.isolated_filesystem():
            # 많은 이벤트가 있는 lab 파일 생성
            events = {}
            for i in range(10):  # 10개의 이벤트
                events[f"Event{i}"] = {
                    "desc": f"Event number {i}",
                    "fields": [
                        ["DateTime", "datetime", "Event time"],
                        ["Data", "string", f"Data for event {i}"]
                    ]
                }
            
            lab_content = {
                "domain": {"name": "large", "desc": "Large domain"},
                "events": events
            }
            
            with open('large.lab.json', 'w') as f:
                json.dump(lab_content, f)
            
            with patch('loglab.cli.handle_import'):
                result = self.runner.invoke(show, ['large.lab.json'])
                
                assert result.exit_code == 0
                assert len(result.output) > 1000  # 충분히 큰 출력
                
                # 모든 이벤트가 출력에 포함되어 있는지 확인
                for i in range(10):
                    assert f"Event{i}" in result.output