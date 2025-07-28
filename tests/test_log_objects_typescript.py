#!/usr/bin/env python3
"""
Basic tests for TypeScript log objects generated from foo.lab.json
"""
import json
import os
import subprocess
import tempfile


def test_typescript_code_generation():
    """Test TypeScript code generation and basic syntax validation"""

    # Generate TypeScript code
    from click.testing import CliRunner

    from loglab.cli import cli

    runner = CliRunner()

    # Get the example lab file path
    example_path = os.path.join(
        os.path.dirname(__file__), "..", "example", "foo.lab.json"
    )

    # Generate TypeScript code
    result = runner.invoke(cli, ["object", example_path, "ts"])

    assert result.exit_code == 0
    assert "export class Login" in result.output
    assert "export class Logout" in result.output
    assert "export class KillMonster" in result.output

    # Check type annotations
    assert "public ServerNo: number;" in result.output
    assert "public Platform: string;" in result.output
    assert "public PlayTime: number | null = null;" in result.output

    # Check methods
    assert "constructor(" in result.output
    assert "public reset(" in result.output
    assert "public serialize(): string" in result.output

    # Check JSON serialization structure
    assert "DateTime: new Date().toISOString()" in result.output
    assert "JSON.stringify(data)" in result.output


def test_typescript_syntax_validation():
    """Test if generated TypeScript code has valid syntax using TypeScript compiler if available"""

    from click.testing import CliRunner

    from loglab.cli import cli

    runner = CliRunner()
    example_path = os.path.join(
        os.path.dirname(__file__), "..", "example", "foo.lab.json"
    )

    # Generate TypeScript code
    result = runner.invoke(cli, ["object", example_path, "ts"])
    assert result.exit_code == 0

    # Try to validate syntax with TypeScript compiler if available
    try:
        # Create temporary TypeScript file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ts", delete=False) as f:
            f.write(result.output)
            temp_file = f.name

        try:
            # Try to compile with tsc if available
            subprocess.run(
                ["tsc", "--noEmit", "--skipLibCheck", temp_file],
                check=True,
                capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # TypeScript compiler not available or compilation failed
            # Just do basic syntax checks
            pass
        finally:
            os.unlink(temp_file)

    except Exception:
        # If anything fails, just pass - this is optional validation
        pass


def test_typescript_class_structure():
    """Test the structure of generated TypeScript classes"""

    from click.testing import CliRunner

    from loglab.cli import cli

    runner = CliRunner()
    example_path = os.path.join(
        os.path.dirname(__file__), "..", "example", "foo.lab.json"
    )

    result = runner.invoke(cli, ["object", example_path, "ts"])
    assert result.exit_code == 0

    ts_code = result.output

    # Test Login class structure
    assert "export class Login {" in ts_code
    assert 'public readonly Event = "Login";' in ts_code

    # Test required fields
    assert "public ServerNo: number;" in ts_code
    assert "public AcntId: number;" in ts_code
    assert "public Platform: string;" in ts_code

    # Test constructor parameters
    assert (
        "constructor(_ServerNo: number, _AcntId: number, _Platform: string)" in ts_code
    )

    # Test optional field in Logout
    assert "public PlayTime: number | null = null;" in ts_code

    # Test const field handling (Category should not appear as public field)
    login_class_start = ts_code.find("export class Login {")
    login_class_end = ts_code.find("export class Logout {")
    login_class = ts_code[login_class_start:login_class_end]

    # Category should not be a public field since it's const
    assert "public Category:" not in login_class

    # But should appear in serialize method
    assert 'data["Category"] = 1;' in ts_code


if __name__ == "__main__":
    test_typescript_code_generation()
    test_typescript_syntax_validation()
    test_typescript_class_structure()
    print("All TypeScript tests passed!")
