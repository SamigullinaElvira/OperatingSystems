import os
import sys
import signal
from subprocess import Popen, PIPE

def sigusr1_handler(signum, frame):
    global expressions_produced
    print(f"Produced: {expressions_produced}")

def main():
    global expressions_produced
    expressions_produced = 0

    signal.signal(signal.SIGUSR1, sigusr1_handler)

    pipe1_to_0 = os.pipe()
    pipe0_to_2 = os.pipe()
    pipe2_to_0 = os.pipe()

    pid_p1 = os.fork()
    if pid_p1 == 0:
        os.close(pipe1_to_0[0])
        os.dup2(pipe1_to_0[1], sys.stdout.fileno())
        os.close(pipe1_to_0[1])
        os.execlp("python3", "producer.py")

    pid_p2 = os.fork()
    if pid_p2 == 0:
        os.close(pipe0_to_2[1])
        os.dup2(pipe0_to_2[0], sys.stdin.fileno())
        os.close(pipe0_to_2[0])

        os.close(pipe2_to_0[0])
        os.dup2(pipe2_to_0[1], sys.stdout.fileno())
        os.close(pipe2_to_0[1])

        os.execlp("/usr/bin/bc", "bc")

    os.close(pipe1_to_0[1])
    os.close(pipe0_to_2[0])
    os.close(pipe2_to_0[1])

    while True:
        expression = os.read(pipe1_to_0[0], 100).decode("utf-8")
        if not expression:
            break

        os.write(pipe0_to_2[1], expression.encode("utf-8"))

        result = os.read(pipe2_to_0[0], 100).decode("utf-8").strip()
        print(f"{expression.strip()} = {result}")
        expressions_produced += 1

    os.kill(pid_p1, signal.SIGTERM)
    os.kill(pid_p2, signal.SIGTERM)

main()
