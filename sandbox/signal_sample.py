import signal
import time


class A:
  def __init__(self):
    self.RUNNING = 1
    signal.signal(signal.SIGINT, self.shutdown)

  def shutdown(self, signum, frame):
    print("")
    print(signum, frame)
    self.RUNNING = 0


def main():
  a = A()

  while a.RUNNING:
    print(a.RUNNING)
    time.sleep(1)


if __name__ == '__main__':
  main()
