import math
import time
from datetime import datetime, timedelta


def main():
  """
  ○○秒ちょうどに何か実行する

  :return:
  """
  delta = timedelta(seconds=1)

  diffs = []
  for i in range(10):
    start = datetime.now()
    start += delta
    start = start.replace(microsecond=0)

    diff = start - datetime.now()
    diff_sec = diff.seconds + (diff.microseconds / 1000000)
    time.sleep(diff_sec)
    now = datetime.now()
    diff = now - start
    print("start:{}\tnow:{}\tdiff:{}".format(start, now,
                                             diff.microseconds / 1000000))
    diffs.append(diff.microseconds / 1000000)
  return (sum(diffs) / len(diffs))


def main2():
  diffs = []
  for i in range(10):
    start = math.floor(time.time() + 1)

    diff = start - time.time()
    time.sleep(diff)
    now = time.time()
    diff = now - start
    print("start:{}\tnow:{}\tdiff:{}".format(start, now, diff))
    diffs.append(diff)
  return (sum(diffs) / len(diffs))


if __name__ == '__main__':
  a = main()
  b = main2()

  print("datetime:{:.4f} ms".format(a * 1000))
  print("    time:{:.4f} ms".format(b * 1000))
  print("    diff:{:.4f} ms".format((a - b) * 1000))
