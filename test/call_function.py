import py_debug as d


@d.call_counter
@d.log_args
@d.log_running_time
def func_add(a, b): return a + b


def test_call_debug():
    for a in range(1, 100, 5):
        for b in range(1, -100, -10):
            func_add(a, b)
