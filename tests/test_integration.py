"""Integration tests for multiple decorators used together."""
import logging
import time
from unittest.mock import patch

import pytest

from py_debug import log_running_time, log_args, log_call_counter, reset_call_counters


class TestIntegration:
    """Integration tests for decorators used together."""

    def setup_method(self):
        """Reset call counters before each test."""
        reset_call_counters()

    def test_all_decorators_together(self):
        """Test using all three decorators on the same function."""
        @log_call_counter()
        @log_args()
        @log_running_time()
        def test_func(a, b):
            return a + b

        with patch('py_debug.util.logging.log') as mock_log:
            result = test_func(1, 2)
            
            assert result == 3
            # Should log: running time, args, and call counter
            assert mock_log.call_count >= 3

    def test_decorators_preserve_functionality(self):
        """Test that decorators don't interfere with each other."""
        @log_call_counter(mute_after=1, log_every=2)
        @log_args(level=logging.INFO)
        @log_running_time(level=logging.WARNING)
        def test_func(x):
            return x * 2

        with patch('py_debug.util.logging.log') as mock_log:
            result1 = test_func(5)
            result2 = test_func(10)
            
            assert result1 == 10
            assert result2 == 20
            # Verify all decorators are working
            assert mock_log.call_count >= 3

    def test_multiple_functions_with_decorators(self):
        """Test multiple functions with different decorator combinations."""
        @log_running_time()
        def func_a(x):
            return x + 1

        @log_args()
        def func_b(x, y):
            return x + y

        @log_call_counter()
        def func_c():
            return 42

        with patch('py_debug.util.logging.log') as mock_log:
            assert func_a(1) == 2
            assert func_b(2, 3) == 5
            assert func_c() == 42
            
            # All should have logged
            assert mock_log.call_count >= 3

    def test_nested_decorator_order(self):
        """Test that decorator order matters and works correctly."""
        call_order = []

        def make_tracker(name):
            def decorator(func):
                def wrapper(*args, **kwargs):
                    call_order.append(name)
                    return func(*args, **kwargs)
                return wrapper
            return decorator

        @make_tracker('counter')
        @make_tracker('args')
        @make_tracker('time')
        def test_func():
            return True

        test_func()
        # Decorators are applied bottom-up, so execution is top-down
        assert call_order == ['counter', 'args', 'time']
