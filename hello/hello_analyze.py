# hello_analyze.py
# tries to find optimum values for number of mutations and mutation rate

from hello import *
import pylab

def test1():
    x = []
    y = []
    for n in range(10, 90, 2):
        c = repeat_run('hello world', 100, n, 200, 10)
        print 'Req %d gen with %d percent mutations' % (c, n)
        x.append(n)
        y.append(c)
    pylab.plot(x, y)
    pylab.show()


if __name__ == '__main__':
    test1()