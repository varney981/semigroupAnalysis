import sys
import time

for i in range(1,11):
  print "{0} out of 11\r".format(i),
  sys.stdout.flush()
  time.sleep(5)
