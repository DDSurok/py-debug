"""Unit tests for edge cases and boundary conditions."""
import logging
from unittest.mock import patch

import pytest

from py_debug import log_call_counter, log_running_time, log_args, reset_call_counters, get_call_count


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""

    def setup_method(self):
        """Reset call counters before each test."""
        reset_call_counters()

    def test_log_call_counter_boundary_log_every(self):
        """Test log_call_counter at log_every boundary."""
        @log_call_counter(mute_after=0, log_every=5)
        def test_func():
            return True

        with patch('py_debug.logging.log') as mock_log:
            # Call 5 should be logged
            for i in range(1, 6):
                test_func()
            
            # Should log exactly once (at call 5)
            assert mock_log.call_count == 1

    def test_log_call_counter_exactly_at_log_every(self):
        """Test log_call_counter when count is exactly divisible by log_every."""
        @log_call_counter(mute_after=2, log_every=5)
        def test_func():
            return True

        with patch('py_debug.logging.log') as mock_log:
            # Calls 1, 2 (mute_after), 5, 10 should be logged
            for i in range(1, 11):
                test_func()
            
            # Should log: 1, 2, 5, 10 = 4 times
            assert mock_log.call_count == 4

    def test_log_running_time_zero_time(self):
        """Test log_running_time handles very fast execution."""
        @log_running_time()
        def test_func():
            pass  # Very fast function

        with patch('py_debug.logging.log') as mock_log:
            test_func()
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            # Should log time even if very small
            assert 'completed in' in log_message

    def test_log_args_with_special_characters(self):
        """Test log_args with special characters in arguments."""
        @log_args()
        def test_func(msg):
            return msg

        with patch('py_debug.logging.log') as mock_log:
            result = test_func("Hello\nWorld\tTest")
            assert result == "Hello\nWorld\tTest"
            assert mock_log.called

    def test_log_args_with_empty_list_and_dict(self):
        """Test log_args with empty list and dict."""
        @log_args()
        def test_func(a, b):
            return a, b

        with patch('py_debug.logging.log') as mock_log:
            result = test_func([], {})
            assert result == ([], {})
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'args = ' in log_message

    def test_log_call_counter_mute_after_one(self):
        """Test log_call_counter with mute_after=1."""
        @log_call_counter(mute_after=1, log_every=10)
        def test_func():
            return True

        with patch('py_debug.logging.log') as mock_log:
            test_func()  # Call 1 - logged
            test_func()  # Call 2 - muted
            test_func()  # Call 3 - muted
            
            assert mock_log.call_count == 1

    def test_log_call_counter_log_every_one(self):
        """Test log_call_counter with log_every=1 (log every call)."""
        @log_call_counter(mute_after=0, log_every=1)
        def test_func():
            return True

        with patch('py_debug.logging.log') as mock_log:
            for i in range(5):
                test_func()
            
            # Should log every call
            assert mock_log.call_count == 5

    def test_log_running_time_with_none_return(self):
        """Test log_running_time with function returning None."""
        @log_running_time()
        def test_func():
            return None

        with patch('py_debug.logging.log') as mock_log:
            result = test_func()
            assert result is None
            assert mock_log.called

    def test_log_args_with_star_args(self):
        """Test log_args with *args and **kwargs."""
        @log_args()
        def test_func(*args, **kwargs):
            return len(args) + len(kwargs)

        with patch('py_debug.logging.log') as mock_log:
            result = test_func(1, 2, 3, x=4, y=5)
            assert result == 5
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'args = ' in log_message
            assert 'kwargs = ' in log_message

    def test_log_call_counter_large_numbers(self):
        """Test log_call_counter with large call counts."""
        @log_call_counter(mute_after=0, log_every=100)
        def test_func():
            return True

        with patch('py_debug.logging.log') as mock_log:
            # Make 250 calls, should log at 100, 200
            for i in range(250):
                test_func()
            
            # Should log at 100, 200 = 2 times
            assert mock_log.call_count == 2

    def test_all_decorators_with_complex_function(self):
        """Test all decorators with a complex function."""
        @log_call_counter()
        @log_args()
        @log_running_time()
        def complex_func(a, b, c=10, *args, **kwargs):
            result = a + b + c
            for arg in args:
                result += arg
            for value in kwargs.values():
                result += value
            return result

        with patch('py_debug.logging.log') as mock_log:
            result = complex_func(1, 2, 3, 4, 5, x=6, y=7)
            assert result == 28
            assert mock_log.call_count >= 3
