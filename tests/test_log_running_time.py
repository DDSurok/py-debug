"""Unit tests for log_running_time decorator."""
import logging
import time
from unittest.mock import patch

import pytest

from py_debug import log_running_time


class TestLogRunningTime:
    """Test cases for log_running_time decorator."""

    def test_logs_execution_time(self):
        """Test that the decorator logs execution time."""
        @log_running_time()
        def test_func():
            time.sleep(0.01)
            return 42

        with patch('logging.log') as mock_log:
            result = test_func()
            
            assert result == 42
            assert mock_log.called
            log_call_args = mock_log.call_args
            assert log_call_args[0][0] == logging.DEBUG
            assert 'is completed in' in log_call_args[0][1]
            assert 'test_func' in log_call_args[0][1]

    def test_returns_correct_value(self):
        """Test that the decorator returns the original function's return value."""
        @log_running_time()
        def test_func():
            return "test_result"

        result = test_func()
        assert result == "test_result"

    def test_preserves_function_metadata(self):
        """Test that functools.wraps preserves function metadata."""
        @log_running_time()
        def test_func():
            """Test docstring."""
            pass

        assert test_func.__name__ == 'test_func'
        assert 'Test docstring' in test_func.__doc__

    def test_with_different_log_levels(self):
        """Test decorator with different logging levels."""
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]
        
        for level in levels:
            @log_running_time(level=level)
            def test_func():
                return True

            with patch('logging.log') as mock_log:
                test_func()
                assert mock_log.called
                assert mock_log.call_args[0][0] == level

    def test_with_invalid_log_level(self):
        """Test decorator with invalid log level."""
        @log_running_time(level=99999)
        def test_func():
            return True

        with patch('logging.warning') as mock_warning:
            test_func()
            assert mock_warning.called
            assert 'Invalid log level' in mock_warning.call_args[0][0]

    def test_with_function_args(self):
        """Test decorator works with functions that have arguments."""
        @log_running_time()
        def test_func(a, b):
            return a + b

        with patch('logging.log') as mock_log:
            result = test_func(1, 2)
            assert result == 3
            assert mock_log.called

    def test_with_function_kwargs(self):
        """Test decorator works with functions that have keyword arguments."""
        @log_running_time()
        def test_func(x=1, y=2):
            return x * y

        with patch('logging.log') as mock_log:
            result = test_func(x=3, y=4)
            assert result == 12
            assert mock_log.called

    def test_time_measurement_accuracy(self):
        """Test that time measurement is reasonably accurate."""
        @log_running_time()
        def test_func():
            time.sleep(0.1)
            return True

        with patch('logging.log') as mock_log:
            test_func()
            log_message = mock_log.call_args[0][1]
            # Extract time from log message
            import re
            time_match = re.search(r'is completed in ([\d.]+)', log_message)
            if time_match:
                elapsed = float(time_match.group(1))
                # Should be approximately 0.1 seconds (with some tolerance)
                assert 0.05 <= elapsed <= 0.2

    def test_exception_handling(self):
        """Test that exceptions are logged and re-raised."""
        @log_running_time()
        def test_func():
            raise ValueError("Test error")

        with patch('logging.log') as mock_log:
            with pytest.raises(ValueError, match="Test error"):
                test_func()
            
            # Should log the exception
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'failed' in log_message or 'ValueError' in log_message

    def test_exception_with_invalid_log_level(self):
        """Test exception handling with invalid log level."""
        @log_running_time(level=99999)
        def test_func():
            raise ValueError("Test error")

        with patch('logging.warning') as mock_warning:
            with pytest.raises(ValueError, match="Test error"):
                test_func()
            
            # Should log warning about invalid log level
            assert mock_warning.called

    def test_very_fast_function(self):
        """Test decorator with a very fast function."""
        @log_running_time()
        def test_func():
            return 42

        with patch('logging.log') as mock_log:
            result = test_func()
            assert result == 42
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'completed in' in log_message

    def test_exception_logs_time(self):
        """Test that log_running_time logs time even when exception occurs."""
        @log_running_time()
        def test_func():
            time.sleep(0.01)
            raise ValueError("Test error")

        with patch('logging.log') as mock_log:
            with pytest.raises(ValueError):
                test_func()
            
            # Should log the failure with time
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'failed' in log_message
            assert 'seconds' in log_message
