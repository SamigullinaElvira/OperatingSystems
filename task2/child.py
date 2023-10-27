import os
import sys
import time
import random

s = int(sys.argv[1])
pid = os.getpid()
ppid = os.getppid()

print(f'Child[{pid}]: I am started. My PID {pid}. Parent PID {ppid}.')
time.sleep(s)
print(f'Child[{pid}]: I am ended. PID {pid}. Parent PID {ppid}.')

os._exit(random.randint(0, 1))
