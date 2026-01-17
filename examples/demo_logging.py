#!/usr/bin/env python3
"""
Demo script showing py_debug decorators with console logging.

This script demonstrates how to use py_debug decorators with logging
configured to print to the console.
"""
import logging
import time

# Configure logging to print to console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

from py_debug import log_running_time, log_args, log_call_counter, reset_call_counters


def main():
    """Main demo function."""
    print("="*70)
    print("py_debug - Logging Decorators Demo")
    print("="*70)
    
    # Example 1: log_running_time
    print("\n1. log_running_time decorator:")
    print("-" * 70)
    
    @log_running_time()
    def calculate_factorial(n):
        """Calculate factorial of n."""
        result = 1
        for i in range(1, n + 1):
            result *= i
            time.sleep(0.01)  # Simulate work
        return result
    
    result = calculate_factorial(5)
    print(f"Factorial of 5: {result}")

    print("\nWaiting 1 second.")
    time.sleep(1)
    print("\n")
    
    # Example 2: log_args
    print("\n2. log_args decorator:")
    print("-" * 70)
    
    @log_args()
    def add_numbers(a, b, c=0):
        """Add numbers."""
        return a + b + c
    
    add_numbers(10, 20)
    add_numbers(5, 15, c=10)
    add_numbers(a=1, b=2, c=3)
    
    print("\nWaiting 1 second.")
    time.sleep(1)
    print("\n")

    # Example 3: log_call_counter
    print("\n3. log_call_counter decorator:")
    print("-" * 70)
    
    reset_call_counters()
    
    @log_call_counter(mute_after=2, log_every=5)
    def process_data(item):
        """Process a data item."""
        return item * 2
    
    print("Processing 12 items (first 2 logged, then every 5th):")
    for i in range(1, 13):
        process_data(i)

    print("\nWaiting 1 second.")
    time.sleep(1)
    print("\n")

    # Example 4: All decorators together
    print("\n4. All decorators together:")
    print("-" * 70)
    
    reset_call_counters()
    
    @log_call_counter(mute_after=1, log_every=3)
    @log_args(level=logging.INFO)
    @log_running_time(level=logging.WARNING)
    def complex_operation(x, y, operation='add'):
        """Perform a complex operation."""
        time.sleep(0.05)
        if operation == 'add':
            return x + y
        elif operation == 'multiply':
            return x * y
        else:
            return x - y
    
    complex_operation(10, 5)
    complex_operation(20, 3, operation='multiply')
    complex_operation(100, 25, operation='subtract')

    print("\nWaiting 1 second.")
    time.sleep(1)
    print("\n")

    # Example 5: Different log levels
    print("\n5. Different log levels:")
    print("-" * 70)
    
    @log_running_time(level=logging.DEBUG)
    def debug_function():
        return "DEBUG"
    
    @log_running_time(level=logging.INFO)
    def info_function():
        return "INFO"
    
    @log_running_time(level=logging.WARNING)
    def warning_function():
        return "WARNING"
    
    debug_function()
    info_function()
    warning_function()

    print("\nWaiting 1 second.")
    time.sleep(1)
    print("\n")

    # Example 6: Exception handling
    print("\n6. Exception handling:")
    print("-" * 70)
    
    @log_running_time()
    def risky_function(value):
        """A function that might fail."""
        if value < 0:
            raise ValueError("Value must be positive")
        return value * 2
    
    try:
        risky_function(5)
        risky_function(-1)
    except ValueError as e:
        print(f"Exception caught: {e}")
    
    print("\n" + "="*70)
    print("Demo complete!")
    print("="*70)


if __name__ == '__main__':
    main()
