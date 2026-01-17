# py-debugs
Debug utils for Python

## Install
    pip install py-debugs

## Using
    import py_debug as d
    import logging  # optional

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        stream=sys.stdout,
        force=True  # Override any existing configuration
    )
    
    @d.log_call_counter(mute_after=1, log_every=100)
    def counter(i):
        pass
    
    
    if __name__ == '__main__':
        for i in range(10000):
            counter(i)
        print(d.get_call_count(counter))

# See also

For more usage examples, see the "examples" catalog.