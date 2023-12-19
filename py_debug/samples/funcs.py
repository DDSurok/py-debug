import py_debug as debug


@debug.call_counter
@debug.log_args
@debug.log_running_time
def func_add(a, b): return a + b
