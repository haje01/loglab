"""확장된 util 모듈 테스트."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest

from loglab.util import (
    AttrDict,
    get_dt_desc,
    get_object_warn,
    get_translator,
    load_file_from,
)


class TestTranslation:
    """번역 기능 테스트."""

    def test_get_translator_none(self):
        """언어가 None일 때 원본 반환."""
        trans = get_translator(None)
        assert trans("test") == "test"

    def test_get_dt_desc_korean(self):
        """한국어 DateTime 설명."""
        desc = get_dt_desc(None)
        assert "이벤트 일시" in desc

    def test_get_object_warn_returns_warning(self):
        """객체 경고 메시지 반환."""
        warn = get_object_warn(None)
        assert isinstance(warn, str)
        assert len(warn) > 0


class TestFileOperations:
    """파일 관련 기능 테스트."""

    def test_load_file_from_existing(self):
        """존재하는 파일 로드."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf8") as f:
            f.write('{"test": "data"}')
            temp_path = f.name

        try:
            content = load_file_from(temp_path)
            assert '{"test": "data"}' in content
        finally:
            os.unlink(temp_path)

    def test_load_file_from_nonexistent(self):
        """존재하지 않는 파일 로드."""
        with pytest.raises(FileNotFoundError):
            load_file_from("/nonexistent/file.json")

    def test_load_file_from_url(self):
        """URL에서 파일 로드."""
        mock_response = Mock()
        mock_response.read.return_value = '{"url": "content"}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=None)

        with patch("loglab.util.urlopen", return_value=mock_response):
            content = load_file_from("http://example.com/test.json")
            assert '{"url": "content"}' in content


class TestAttrDict:
    """AttrDict 클래스 테스트."""

    def test_attrdict_basic(self):
        """기본 AttrDict 기능."""
        data = AttrDict({"key": "value", "nested": {"inner": "data"}})
        assert data.key == "value"
        assert data["key"] == "value"
        assert data.nested.inner == "data"

    def test_attrdict_assignment(self):
        """AttrDict 값 할당."""
        data = AttrDict()
        data.new_key = "new_value"
        assert data["new_key"] == "new_value"

    def test_attrdict_nested_creation(self):
        """중첩된 AttrDict 생성."""
        data = AttrDict({"level1": {"level2": {"level3": "deep"}}})
        assert data.level1.level2.level3 == "deep"


class TestFileLoading:
    """파일 로딩 추가 테스트."""

    def test_load_file_with_url(self):
        """URL에서 파일 로드 (실제 테스트는 mock 사용)."""
        with patch("loglab.util.urlopen") as mock_urlopen:
            mock_response = Mock()
            mock_response.read.return_value = '{"test": "content"}'
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=None)
            mock_urlopen.return_value = mock_response

            content = load_file_from("http://example.com/test.json")
            assert '{"test": "content"}' in content


class TestPathOperations:
    """경로 관련 기능 테스트."""

    def test_builtin_types_constant(self):
        """내장 타입 상수 확인."""
        from loglab.util import BUILTIN_TYPES

        expected_types = ("string", "integer", "number", "boolean", "datetime")
        assert BUILTIN_TYPES == expected_types

    def test_loglab_home_path(self):
        """LOGLAB_HOME 경로 확인."""
        from loglab.util import LOGLAB_HOME

        assert isinstance(LOGLAB_HOME, Path)
        assert LOGLAB_HOME.exists()


class TestErrorHandling:
    """에러 처리 테스트."""

    def test_load_file_encoding_error(self):
        """인코딩 에러 처리."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            f.write(b"\xff\xfe\x00\x00")  # Invalid UTF-8
            temp_path = f.name

        try:
            with pytest.raises(UnicodeDecodeError):
                load_file_from(temp_path)
        finally:
            os.unlink(temp_path)
