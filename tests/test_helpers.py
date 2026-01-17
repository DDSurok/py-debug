"""Unit tests for helper functions."""
import pytest

from py_debug import log_call_counter, reset_call_counters, get_call_count


class TestHelperFunctions:
    """Test cases for helper functions."""

    def test_reset_call_counters(self):
        """Test that reset_call_counters clears all counters."""
        @log_call_counter()
        def test_func():
            return True

        test_func()
        test_func()
        assert get_call_count(test_func) == 2

        reset_call_counters()
        assert get_call_count(test_func) == 0

    def test_get_call_count(self):
        """Test that get_call_count returns correct count."""
        @log_call_counter()
        def test_func():
            return True

        assert get_call_count(test_func) == 0

        test_func()
        assert get_call_count(test_func) == 1

        test_func()
        test_func()
        assert get_call_count(test_func) == 3

    def test_get_call_count_never_called(self):
        """Test get_call_count for function that was never called."""
        def test_func():
            return True

        assert get_call_count(test_func) == 0

    def test_reset_affects_multiple_functions(self):
        """Test that reset affects all functions."""
        @log_call_counter()
        def func_a():
            return 'a'

        @log_call_counter()
        def func_b():
            return 'b'

        func_a()
        func_a()
        func_b()
        func_b()
        func_b()

        assert get_call_count(func_a) == 2
        assert get_call_count(func_b) == 3

        reset_call_counters()

        assert get_call_count(func_a) == 0
        assert get_call_count(func_b) == 0
