"""Unit tests for internal helper functions."""
import logging
from unittest.mock import patch

import pytest

# Import internal functions for testing
# These are not in __all__, so we import directly from the module
import py_debug
from py_debug import _is_valid_log_level, _get_function_name, _format_args_info


class TestIsValidLogLevel:
    """Test cases for _is_valid_log_level helper function."""

    def test_valid_log_levels(self):
        """Test that valid log levels return True."""
        valid_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]
        
        for level in valid_levels:
            assert _is_valid_log_level(level) is True

    def test_invalid_log_level(self):
        """Test that invalid log levels return False."""
        assert _is_valid_log_level(99999) is False
        assert _is_valid_log_level(-1) is False

    def test_type_error_handling(self):
        """Test that TypeError is handled gracefully."""
        # Mock logging.getLevelName to raise TypeError
        with patch('logging.getLevelName', side_effect=TypeError):
            assert _is_valid_log_level(123) is False

    def test_attribute_error_handling(self):
        """Test that AttributeError is handled gracefully."""
        # Mock logging.getLevelName to raise AttributeError
        with patch('logging.getLevelName', side_effect=AttributeError):
            assert _is_valid_log_level(123) is False


class TestGetFunctionName:
    """Test cases for _get_function_name helper function."""

    def test_standard_function(self):
        """Test getting name for a standard function."""
        def test_func():
            pass
        
        name = _get_function_name(test_func)
        assert 'test_func' in name
        assert '.' in name  # Should include module name

    def test_nested_function(self):
        """Test getting name for a nested function."""
        def outer():
            def inner():
                pass
            return inner
        
        inner_func = outer()
        name = _get_function_name(inner_func)
        assert 'inner' in name


class TestFormatArgsInfo:
    """Test cases for _format_args_info helper function."""

    def test_no_args_no_kwargs(self):
        """Test formatting with no arguments."""
        result = _format_args_info((), {})
        assert result == 'without args'

    def test_args_only(self):
        """Test formatting with positional args only."""
        result = _format_args_info((1, 2, 3), {})
        assert 'args = ' in result
        assert 'kwargs' not in result or 'and' not in result

    def test_kwargs_only(self):
        """Test formatting with kwargs only."""
        result = _format_args_info((), {'x': 1, 'y': 2})
        assert 'kwargs = ' in result
        assert 'and' not in result

    def test_both_args_and_kwargs(self):
        """Test formatting with both args and kwargs."""
        result = _format_args_info((1, 2), {'x': 3})
        assert 'args = ' in result
        assert 'kwargs = ' in result
        assert 'and' in result

    def test_empty_args_with_kwargs(self):
        """Test formatting with empty tuple args and kwargs."""
        result = _format_args_info((), {'key': 'value'})
        assert 'kwargs = ' in result

    def test_args_with_empty_kwargs(self):
        """Test formatting with args and empty kwargs."""
        result = _format_args_info((1, 2), {})
        assert 'args = ' in result

    def test_complex_types(self):
        """Test formatting with complex argument types."""
        result = _format_args_info(([1, 2], {'nested': 'dict'}), {'key': 'value'})
        assert 'args = ' in result
        assert 'kwargs = ' in result
