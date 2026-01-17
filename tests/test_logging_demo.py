"""Demonstration tests showing actual logging output to console."""
import logging
import time

from py_debug import log_running_time, log_args, log_call_counter, reset_call_counters


class TestLoggingDemo:
    """Demo tests that show actual logging output (not mocked)."""

    def setup_method(self):
        """Setup logging for each test."""
        # Configure logging to show output on console
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S',
            force=True
        )
        reset_call_counters()

    def test_demo_log_running_time(self):
        """Demonstrate log_running_time with console output."""
        print("\n" + "="*60)
        print("Demo: log_running_time decorator")
        print("="*60)
        
        @log_running_time()
        def calculate_sum(n):
            """Calculate sum of numbers from 1 to n."""
            total = sum(range(1, n + 1))
            time.sleep(0.1)  # Simulate some work
            return total
        
        result = calculate_sum(100)
        print(f"Result: {result}\n")

    def test_demo_log_args(self):
        """Demonstrate log_args with console output."""
        print("\n" + "="*60)
        print("Demo: log_args decorator")
        print("="*60)
        
        @log_args(level=logging.INFO)
        def add_numbers(a, b, multiplier=1):
            """Add two numbers with optional multiplier."""
            return (a + b) * multiplier
        
        result1 = add_numbers(5, 3)
        result2 = add_numbers(10, 20, multiplier=2)
        result3 = add_numbers(a=15, b=25)  # Using kwargs
        print(f"Results: {result1}, {result2}, {result3}\n")

    def test_demo_log_call_counter(self):
        """Demonstrate log_call_counter with console output."""
        print("\n" + "="*60)
        print("Demo: log_call_counter decorator")
        print("="*60)
        
        @log_call_counter(mute_after=2, log_every=5)
        def process_item(item):
            """Process an item."""
            return item * 2
        
        print("Processing 15 items (first 2 logged, then every 5th):")
        for i in range(1, 16):
            process_item(i)
        print()

    def test_demo_all_decorators(self):
        """Demonstrate all decorators together with console output."""
        print("\n" + "="*60)
        print("Demo: All decorators together")
        print("="*60)
        
        @log_call_counter(mute_after=1, log_every=2)
        @log_args(level=logging.INFO)
        @log_running_time(level=logging.WARNING)
        def complex_calculation(x, y, operation='add'):
            """Perform a complex calculation."""
            time.sleep(0.05)
            if operation == 'add':
                return x + y
            elif operation == 'multiply':
                return x * y
            else:
                return x - y
        
        result1 = complex_calculation(10, 5)
        result2 = complex_calculation(20, 3, operation='multiply')
        print(f"Results: {result1}, {result2}\n")

    def test_demo_different_log_levels(self):
        """Demonstrate different log levels."""
        print("\n" + "="*60)
        print("Demo: Different log levels")
        print("="*60)
        
        # Set logging to show all levels
        logging.getLogger().setLevel(logging.DEBUG)
        
        @log_running_time(level=logging.DEBUG)
        def debug_func():
            return "DEBUG level"
        
        @log_running_time(level=logging.INFO)
        def info_func():
            return "INFO level"
        
        @log_running_time(level=logging.WARNING)
        def warning_func():
            return "WARNING level"
        
        @log_running_time(level=logging.ERROR)
        def error_func():
            return "ERROR level"
        
        debug_func()
        info_func()
        warning_func()
        error_func()
        print()

    def test_demo_exception_handling(self):
        """Demonstrate exception handling with logging."""
        print("\n" + "="*60)
        print("Demo: Exception handling")
        print("="*60)
        
        @log_running_time()
        def risky_function(value):
            """A function that might raise an exception."""
            if value < 0:
                raise ValueError("Value must be positive")
            return value * 2
        
        try:
            risky_function(5)
            risky_function(-1)  # This will raise an exception
        except ValueError as e:
            print(f"Caught exception: {e}\n")
