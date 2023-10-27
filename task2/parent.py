from os import fork, getpid, wait, execv
from sys import argv
from random import randint

n = int(argv[1])

for i in range(n):
    child = fork()
    if child == 0:
        number = randint(5, 10)
        print(f"Parent[{getpid()}]: I ran children process with PID {getpid()}.")
        execv('/usr/bin/python3', ['python3', 'child.py', str(number)])
    else:
        ret = wait()
        if ret[1] == 0:
            print(f"Parent[{getpid()}]: Child with PID {ret[0]} terminated. Exit Status {ret[1]}.")
        else:
            print(f"Parent[{getpid()}]: Child with PID {ret[0]} terminated. Exit Status {ret[1]}. Starting a new child process.")

