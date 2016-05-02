import math as m
import numpy as np
# calculate the population standard deviation
def stdev_p(data):
    sum = 0
    for x in data:
        sum = sum + x

    n = len(data)
    mean = sum / n

    sum = 0
    for x in data:
        sum = sum + (x - mean)**2

    sd = m.sqrt(sum / n)

    return sd

# calculate the sample standard deviation
def stdev_s(data):
    sum = 0
    for x in data:
        sum = sum + x

    n = len(data)
    mean = sum / n

    sum = 0
    for x in data:
        sum = sum + (x - mean)**2

    sd = m.sqrt(sum / (n - 1))

    return sd


if __name__ == "__main__":
    test = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    print "the population stdev is", stdev_p(test)
    print "the sample stdev is", stdev_s(test)
    print "the np population stdev is", np.std(test)
    print "the np sample stdev is", np.std(test, ddof=1)
