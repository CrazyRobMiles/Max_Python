## Example 9 uses locks to control access to the print function

import _thread
import time

print_lock = _thread.allocate_lock()

def core1_task():
    while True:
        with print_lock:
            print("Hello from core 1")
        time.sleep(0.6)
        
# Start Core 1 thread
_thread.start_new_thread(core1_task, ())

while True:
    with print_lock:
        print("Hello from core 2")
    time.sleep(0.5)

