import sys

try:
  sys.exit()
finally:
  print('printed')

print("not printed")
