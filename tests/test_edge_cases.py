"""Unit tests for edge cases and boundary conditions."""
import logging
from unittest.mock import patch

import pytest

from py_debug import log_call_counter, log_running_time, log_args, reset_call_counters


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""

    def setup_method(self):
        """Reset call counters before each test."""
        reset_call_counters()

    def test_log_call_counter_mute_after_zero(self):
        """Test log_call_counter with mute_after=0 (no initial logging)."""
        @log_call_counter(mute_after=0, log_every=3)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            # Calls 3, 6, 9 should be logged (no initial calls)
            for i in range(1, 10):
                test_func()
            
            # Should log at calls 3, 6, 9 = 3 times
            assert mock_log.call_count == 3

    def test_log_call_counter_boundary_mute_after(self):
        """Test log_call_counter at mute_after boundary."""
        @log_call_counter(mute_after=3, log_every=10)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            # Calls 1, 2, 3 should be logged, 4 should not
            test_func()  # 1 - logged
            test_func()  # 2 - logged
            test_func()  # 3 - logged
            test_func()  # 4 - muted
            
            assert mock_log.call_count == 3

    def test_log_call_counter_boundary_log_every(self):
        """Test log_call_counter at log_every boundary."""
        @log_call_counter(mute_after=0, log_every=5)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
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

        with patch('py_debug.util.logging.log') as mock_log:
            # Calls 1, 2 (mute_after), 5, 10 should be logged
            for i in range(1, 11):
                test_func()
            
            # Should log: 1, 2, 5, 10 = 4 times
            assert mock_log.call_count == 4

    def test_log_running_time_very_fast_function(self):
        """Test log_running_time with a very fast function."""
        @log_running_time()
        def test_func():
            return 42

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func()
            assert result == 42
            assert mock_log.called
            # Should still log even for very fast functions
            log_message = mock_log.call_args[0][1]
            assert 'completed in' in log_message

    def test_log_args_with_none_values(self):
        """Test log_args with None values in arguments."""
        @log_args()
        def test_func(a, b=None):
            return a, b

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func(1, None)
            assert result == (1, None)
            assert mock_log.called

    def test_log_args_with_empty_list_and_dict(self):
        """Test log_args with empty list and dict."""
        @log_args()
        def test_func(a, b):
            return a, b

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func([], {})
            assert result == ([], {})
            assert mock_log.called
            log_message = mock_log.call_args[0][1]
            assert 'args = ' in log_message

    def test_log_call_counter_with_mute_after_greater_than_log_every(self):
        """Test log_call_counter when mute_after > log_every."""
        @log_call_counter(mute_after=10, log_every=5)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            # Calls 1-10 (mute_after), 15, 20 (log_every) should be logged
            for i in range(1, 21):
                test_func()
            
            # Should log: 1-10 (10 times), 15, 20 (2 times) = 12 times
            assert mock_log.call_count == 12

    def test_log_call_counter_single_call(self):
        """Test log_call_counter with a single call."""
        @log_call_counter(mute_after=5)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            test_func()
            # Single call should be logged (within mute_after)
            assert mock_log.call_count == 1

    def test_log_running_time_with_zero_time(self):
        """Test log_running_time handles very fast execution."""
        @log_running_time()
        def test_func():
            pass  # Very fast function

        with patch('py_debug.util.logging.log') as mock_log:
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

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func("Hello\nWorld\tTest")
            assert result == "Hello\nWorld\tTest"
            assert mock_log.called

    def test_log_call_counter_reset_during_execution(self):
        """Test that reset_call_counters works correctly."""
        @log_call_counter()
        def test_func():
            return True

        test_func()
        test_func()
        assert test_func.__module__ is not None  # Ensure function is callable
        
        from py_debug import get_call_count
        assert get_call_count(test_func) == 2
        
        reset_call_counters()
        assert get_call_count(test_func) == 0
        
        # After reset, counter should start from 1
        test_func()
        assert get_call_count(test_func) == 1
