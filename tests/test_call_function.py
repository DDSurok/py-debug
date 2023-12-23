import logging
import time

import py_debug as debug


@debug.log_call_counter()
@debug.log_args()
@debug.log_running_time()
def func_add(a, b): return a + b


@debug.log_running_time(level=logging.INFO)
@debug.log_args(level=logging.WARNING)
def func_long(a): time.sleep(0.01 * a)


logging.basicConfig(level=logging.DEBUG)


def test_call_debug():
    for a in range(1, 100, 5):
        for b in range(1, -100, -10):
            func_add(a, b)
    assert True


def test_call_with_another_level():
    for a in range(20):
        func_long(a=a)


if __name__ == '__main__':
    test_call_debug()
    test_call_with_another_level()
