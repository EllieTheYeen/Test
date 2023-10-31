import sys

def test(*a):
  print(a)
  sys.__excepthook__(*a)

sys.excepthook = test

1/0
