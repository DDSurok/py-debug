# py-debugs
Debug utils for Python

## Install
    pip install py-debugs

## Using
    import py_debug as d
    import logging  # optional

    
    @d.call_counter(mute_after=1, log_every=100)
    def counter(i):
        pass
    
    
    if __name__ == '__main__':
        for i in range(10000):
            counter(i)
