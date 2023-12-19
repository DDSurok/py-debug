import logging

from py_debug.samples.funcs import func_add


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
