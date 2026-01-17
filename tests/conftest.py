"""Pytest configuration for py_debug tests."""
import logging
import sys


def pytest_configure(config):
    """Configure logging for tests."""
    # Configure logging to print to console
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        stream=sys.stdout,
        force=True  # Override any existing configuration
    )


def pytest_runtest_setup(item):
    """Setup before each test."""
    # Optionally configure logging per test
    pass
