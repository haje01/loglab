# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LogLab is a Python tool for designing and validating JSON Lines log formats. It provides:
- Object-oriented, reusable log design capabilities
- Automatic documentation generation from log schemas
- Validation of actual log output against designed schemas
- Code generation for Python, C#, and C++ log objects

## Architecture

The codebase is organized into several core modules:

- `loglab/cli.py` - Command-line interface using Click framework
- `loglab/model.py` - Document Object Model for lab files (schema definitions)
- `loglab/schema.py` - JSON Schema validation and generation
- `loglab/doc.py` - Documentation generation (text and HTML)
- `loglab/util.py` - Utility functions and built-in types

Key concepts:
- **Lab files** (*.lab.json): JSON schema definitions for log formats
- **Domain**: Namespace for organizing log schemas
- **Types**: Custom data types with validation rules
- **Mixins**: Reusable field groups that can be combined
- **Bases**: Base classes for events
- **Events**: Specific log event types with fields

## Development Commands

### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
coverage run --source loglab -m pytest tests

# Run tests across multiple Python versions
tox
```

### Building
```bash
# Build standalone executable
./tools/build.sh
# This runs: pytest tests && pyinstaller ...
```

### Code Generation Testing
```bash
# Generate Python log objects
loglab object example/foo.lab.json py -o tests/loglab_foo.py
cd tests && pytest test_log_objects_python.py

# Generate C# log objects  
loglab object example/foo.lab.json cs -o tests/cstest/loglab_foo.cs
cd tests/cstest && dotnet run

# Generate C++ log objects (requires libgtest-dev)
loglab object example/foo.lab.json cpp -o tests/loglab_foo.h
cd tests && g++ -std=c++17 -I. test_log_objects_cpp.cpp -lgtest -lgtest_main -lpthread -o test_log_objects_cpp && ./test_log_objects_cpp
```

## Key Files and Patterns

- **Entry point**: `bin/loglab` script calls `loglab.cli:cli()`
- **Lab file schema**: `schema/lab.schema.json` defines the structure of lab files
- **Examples**: `example/` directory contains sample lab files
- **Templates**: `template/` directory contains Jinja2 templates for code generation
- **Localization**: `locales/` for internationalization support

## CLI Commands

- `loglab show <labfile>` - Display log schema components
- `loglab html <labfile>` - Generate HTML documentation
- `loglab verify <labfile>` - Validate lab file schema
- `loglab schema <labfile>` - Generate JSON schema from lab file
- `loglab check <labfile> <logfile>` - Validate log file against schema
- `loglab object <labfile> <lang>` - Generate log objects in target language

## Dependencies

Core: click, jsonschema==3.2.0, jinja2, tabulate[widechars], requests
Dev: pytest, coverage, pyinstaller, tox