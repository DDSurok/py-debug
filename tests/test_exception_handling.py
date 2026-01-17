"""Unit tests for exception handling in decorators."""
import logging
from unittest.mock import patch

import pytest

from py_debug import log_running_time, log_args, log_call_counter


class TestExceptionHandling:
    """Test cases for exception handling in decorators."""

    def test_log_args_with_exception(self):
        """Test that log_args doesn't catch exceptions from wrapped function."""
        @log_args()
        def test_func():
            raise ValueError("Test error")

        with patch('py_debug.util.logging.log') as mock_log:
            with pytest.raises(ValueError, match="Test error"):
                test_func()
            
            # Should have logged before the exception
            assert mock_log.called

    def test_log_call_counter_with_exception(self):
        """Test that log_call_counter increments even when function raises exception."""
        @log_call_counter()
        def test_func():
            raise ValueError("Test error")

        with patch('py_debug.util.logging.log'):
            # First call should increment counter
            with pytest.raises(ValueError):
                test_func()
            
            # Second call should also increment
            with pytest.raises(ValueError):
                test_func()
            
            # Counter should be 2 even though both calls failed
            from py_debug import get_call_count
            assert get_call_count(test_func) == 2

    def test_log_running_time_exception_with_invalid_log_level(self):
        """Test log_running_time exception handling with invalid log level."""
        @log_running_time(level=99999)
        def test_func():
            raise ValueError("Test error")

        with patch('py_debug.util.logging.warning') as mock_warning:
            with pytest.raises(ValueError, match="Test error"):
                test_func()
            
            # Should log warning about invalid log level
            assert mock_warning.called

    def test_log_call_counter_exception_with_invalid_log_level(self):
        """Test log_call_counter with exception and invalid log level."""
        @log_call_counter(level=99999, mute_after=0)
        def test_func():
            raise ValueError("Test error")

        with patch('py_debug.util.logging.warning') as mock_warning:
            with pytest.raises(ValueError):
                test_func()
            
            # Should log warning about invalid log level
            assert mock_warning.called

    def test_log_args_exception_with_invalid_log_level(self):
        """Test log_args with exception and invalid log level."""
        @log_args(level=99999)
        def test_func():
            raise ValueError("Test error")

        with patch('py_debug.util.logging.warning') as mock_warning:
            with pytest.raises(ValueError):
                test_func()
            
            # Should log warning about invalid log level
            assert mock_warning.called

    def test_log_running_time_exception_logs_time(self):
        """Test that log_running_time logs time even when exception occurs."""
        @log_running_time()
        def test_func():
            import time
            time.sleep(0.01)
            raise ValueError("Test error")

        with patch('py_debug.util.logging.log') as mock_log:
            with pytest.raises(ValueError):
                test_func()
            
            # Should log the failure with time
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'failed' in log_message
            assert 'seconds' in log_message

    def test_multiple_decorators_with_exception(self):
        """Test that exceptions propagate correctly through multiple decorators."""
        @log_call_counter()
        @log_args()
        @log_running_time()
        def test_func():
            raise ValueError("Test error")

        with patch('py_debug.util.logging.log'):
            with pytest.raises(ValueError, match="Test error"):
                test_func()
            
            # Counter should still increment
            from py_debug import get_call_count
            assert get_call_count(test_func) == 1
