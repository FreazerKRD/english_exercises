import functools
import time
 
def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        time_start = time.perf_counter()
        value = func(*args, **kwargs)
        time_end = time.perf_counter()
        elapsed_time = time_end - time_start
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer