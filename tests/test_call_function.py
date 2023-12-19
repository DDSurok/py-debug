import logging
import py_debug as debug


@debug.call_counter
@debug.log_args
@debug.log_running_time
def func_add(a, b): return a + b


logging.basicConfig(level=logging.DEBUG)


def test_call_debug():
    try:
        for a in range(1, 100, 5):
            for b in range(1, -100, -10):
                func_add(a, b)
        assert True
    except:
        assert False


if __name__ == '__main__':
    test_call_debug()
