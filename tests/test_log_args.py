"""Unit tests for log_args decorator."""
import logging
from unittest.mock import patch

import pytest

from py_debug import log_args


class TestLogArgs:
    """Test cases for log_args decorator."""

    def test_logs_without_args(self):
        """Test logging when function is called without arguments."""
        @log_args()
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            test_func()
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'without args' in log_message
            assert 'test_func' in log_message

    def test_logs_with_positional_args_only(self):
        """Test logging when function is called with positional args only."""
        @log_args()
        def test_func(a, b):
            return a + b

        with patch('py_debug.util.logging.log') as mock_log:
            test_func(1, 2)
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'args = ' in log_message
            assert 'test_func' in log_message

    def test_logs_with_kwargs_only(self):
        """Test logging when function is called with kwargs only."""
        @log_args()
        def test_func(x=1, y=2):
            return x * y

        with patch('py_debug.util.logging.log') as mock_log:
            test_func(x=3, y=4)
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'kwargs = ' in log_message
            assert 'test_func' in log_message

    def test_logs_with_both_args_and_kwargs(self):
        """Test logging when function is called with both args and kwargs."""
        @log_args()
        def test_func(a, b, x=1, y=2):
            return a + b + x + y

        with patch('py_debug.util.logging.log') as mock_log:
            test_func(1, 2, x=3, y=4)
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'args = ' in log_message
            assert 'kwargs = ' in log_message
            assert 'and' in log_message

    def test_returns_correct_value(self):
        """Test that the decorator returns the original function's return value."""
        @log_args()
        def test_func(a, b):
            return a * b

        result = test_func(3, 4)
        assert result == 12

    def test_preserves_function_metadata(self):
        """Test that functools.wraps preserves function metadata."""
        @log_args()
        def test_func():
            """Test docstring."""
            pass

        assert test_func.__name__ == 'test_func'
        assert 'Test docstring' in test_func.__doc__

    def test_with_different_log_levels(self):
        """Test decorator with different logging levels."""
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]
        
        for level in levels:
            @log_args(level=level)
            def test_func():
                return True

            with patch('py_debug.util.logging.log') as mock_log:
                test_func()
                assert mock_log.called
                assert mock_log.call_args[0][0] == level

    def test_with_invalid_log_level(self):
        """Test decorator with invalid log level."""
        @log_args(level=99999)
        def test_func():
            return True

        with patch('py_debug.util.logging.warning') as mock_warning:
            test_func()
            assert mock_warning.called
            assert 'Log level has not found' in mock_warning.call_args[0][0]

    def test_empty_args_and_kwargs(self):
        """Test that empty args and kwargs are handled correctly."""
        @log_args()
        def test_func(*args, **kwargs):
            return len(args) + len(kwargs)

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func()
            assert result == 0
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'without args' in log_message

    def test_complex_args(self):
        """Test with complex argument types."""
        @log_args()
        def test_func(a, b, c):
            return a, b, c

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func([1, 2, 3], {'key': 'value'}, "string")
            assert result == ([1, 2, 3], {'key': 'value'}, "string")
            assert mock_log.called
