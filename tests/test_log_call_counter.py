"""Unit tests for log_call_counter decorator."""
import logging
from unittest.mock import patch

import pytest

from py_debug import log_call_counter, reset_call_counters, get_call_count


class TestLogCallCounter:
    """Test cases for log_call_counter decorator."""

    def setup_method(self):
        """Reset call counters before each test."""
        reset_call_counters()

    def test_counter_increments(self):
        """Test that the counter increments correctly."""
        @log_call_counter()
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            test_func()
            test_func()
            test_func()
            
            # Should log at least once (first call)
            assert mock_log.called
            # Verify counter is incremented
            assert get_call_count(test_func) == 3

    def test_logs_first_calls(self):
        """Test that first calls are logged (mute_after behavior)."""
        @log_call_counter(mute_after=3)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            # First 3 calls should be logged (0, 1, 2)
            test_func()  # Call 1
            test_func()  # Call 2
            test_func()  # Call 3
            
            # Should have logged 3 times
            assert mock_log.call_count == 3

    def test_mutes_after_threshold(self):
        """Test that calls are muted after mute_after threshold."""
        @log_call_counter(mute_after=2, log_every=10)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            test_func()  # Call 1 - logged
            test_func()  # Call 2 - logged
            test_func()  # Call 3 - muted
            test_func()  # Call 4 - muted
            test_func()  # Call 5 - muted
            
            # Should only log first 2 calls
            assert mock_log.call_count == 2

    def test_logs_every_n_calls(self):
        """Test that calls are logged every log_every calls."""
        @log_call_counter(mute_after=0, log_every=5)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            # Call 5, 10, 15, 20 should be logged
            for i in range(1, 21):
                test_func()
            
            # Should log at calls 5, 10, 15, 20
            assert mock_log.call_count == 4

    def test_combination_mute_and_log_every(self):
        """Test combination of mute_after and log_every."""
        @log_call_counter(mute_after=2, log_every=5)
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            # Calls 1, 2 (mute_after), 5, 10, 15, 20 (log_every) should be logged
            for i in range(1, 21):
                test_func()
            
            # Should log: 1, 2, 5, 10, 15, 20 = 6 times
            assert mock_log.call_count == 6

    def test_returns_correct_value(self):
        """Test that the decorator returns the original function's return value."""
        @log_call_counter()
        def test_func(a, b):
            return a + b

        result = test_func(1, 2)
        assert result == 3

    def test_preserves_function_metadata(self):
        """Test that functools.wraps preserves function metadata."""
        @log_call_counter()
        def test_func():
            """Test docstring."""
            pass

        assert test_func.__name__ == 'test_func'
        assert 'Test docstring' in test_func.__doc__

    def test_with_different_log_levels(self):
        """Test decorator with different logging levels."""
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]
        
        for level in levels:
            reset_call_counters()
            
            @log_call_counter(level=level)
            def test_func():
                return True

            with patch('py_debug.util.logging.log') as mock_log:
                test_func()
                assert mock_log.called
                assert mock_log.call_args[0][0] == level

    def test_with_invalid_log_level(self):
        """Test decorator with invalid log level."""
        @log_call_counter(level=99999)
        def test_func():
            return True

        with patch('py_debug.util.logging.warning') as mock_warning:
            test_func()
            assert mock_warning.called
            assert 'Log level has not found' in mock_warning.call_args[0][0]

    def test_multiple_functions_separate_counters(self):
        """Test that different functions have separate counters."""
        @log_call_counter()
        def func_a():
            return 'a'

        @log_call_counter()
        def func_b():
            return 'b'

        with patch('py_debug.util.logging.log'):
            func_a()
            func_a()
            func_b()
            func_b()
            func_b()
        
        assert get_call_count(func_a) == 2
        assert get_call_count(func_b) == 3

    def test_log_message_contains_count(self):
        """Test that log message contains the call count."""
        @log_call_counter()
        def test_func():
            return True

        with patch('py_debug.util.logging.log') as mock_log:
            test_func()
            test_func()
            test_func()
            
            # Check the last log message contains the count
            log_message = mock_log.call_args[0][1]
            assert 'has been called' in log_message
            assert '3 times' in log_message or '3' in log_message

    def test_with_function_args(self):
        """Test decorator works with functions that have arguments."""
        @log_call_counter()
        def test_func(a, b, c=10):
            return a + b + c

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func(1, 2, c=3)
            assert result == 6
            assert mock_log.called

    def test_invalid_mute_after_raises_error(self):
        """Test that negative mute_after raises ValueError."""
        with pytest.raises(ValueError, match="mute_after must be non-negative"):
            @log_call_counter(mute_after=-1)
            def test_func():
                pass

    def test_invalid_log_every_raises_error(self):
        """Test that invalid log_every raises ValueError."""
        with pytest.raises(ValueError, match="log_every must be positive"):
            @log_call_counter(log_every=0)
            def test_func():
                pass
