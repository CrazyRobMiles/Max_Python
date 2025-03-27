## Example 8 run threads on core 0 and core 1 and watch the prints interleave

import _thread
import time

def core1_task():
    while True:
        print("Hello from core 1")
        time.sleep(0.6)
        
# Start Core 1 thread
_thread.start_new_thread(core1_task, ())

while True:
    print("Hello from core 2")
    time.sleep(0.5)
