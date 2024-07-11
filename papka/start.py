import subprocess
import time


def run_test():
    while True:
        test_process = subprocess.Popen(["python", "test.py"])

        time.sleep(3600)

        test_process.terminate()
        test_process.wait()


if __name__ == "__main__":
    run_test()
