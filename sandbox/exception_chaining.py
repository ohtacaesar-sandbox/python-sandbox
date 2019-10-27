class A(Exception):
  pass


class B(Exception):
  pass


def main():
  try:
    raise A('a')
  except A as e:
    raise B('b') from e


if __name__ == '__main__':
  main()
