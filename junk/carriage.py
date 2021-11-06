from time import sleep
import sys

counter = 0
while (counter < 500000):
    if counter % 3000 == 0:
        # sys.stdout.write("Download progress: %i%%   \r" % (counter) )
        # sys.stdout.flush()
        print('Downloading File FooFile.txt: ', counter, '\r', sep='', end="")
    counter = counter + 1
    sleep(0.0005)