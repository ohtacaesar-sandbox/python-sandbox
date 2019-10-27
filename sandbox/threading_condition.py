import random
import signal
import sys
import time
from datetime import datetime
from threading import Thread, Condition, current_thread


def shutdown(signum, frame):
  sys.exit()


def do_something(c: Condition, stopper: list):
  name = current_thread().getName()

  while 1:
    with c:
      c.wait()

    if stopper[0]:
      break

    print("{}({}): Do something !!".format(datetime.now(), name))

  print("{}({}): Finished !!".format(datetime.now(), name))


def main():
  signal.signal(signal.SIGTERM, shutdown)
  signal.signal(signal.SIGINT, shutdown)

  c = Condition()
  stopper = [0]
  threads = [Thread(target=do_something, args=(c, stopper)) for _ in range(3)]
  name = current_thread().getName()

  try:
    [t.start() for t in threads]

    while 1:
      print("")
      with c:
        print("{}({}): Notify all".format(datetime.now(), name))
        c.notify_all()
      time.sleep(random.random() * 2)

  finally:
    print("{}({}): Finally".format(datetime.now(), name))
    stopper[0] = 1
    with c:
      print("{}: Notify all to stop".format(name))
      c.notify_all()
    [t.join(5) for t in threads]


if __name__ == '__main__':
  main()
