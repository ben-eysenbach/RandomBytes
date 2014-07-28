import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
import time
import u3
import serial
import os

class Graph:
    '''Class for displaying the 3 subplots in real time for the hot fire test
    The plots are: Pressure, Gas concentrations, and force'''

    def __init__(self):

        self.interval = 30 #milliseconds per sample
        self.length = 100 #saved points
        self.t = [-float(self.interval)/1000 * k for k in range(self.length, 0, -1)]


        self.acc1 = [0] * self.length
        self.acc2 = [0] * self.length
        self.acc3 = [0] * self.length

        self.rot1 = [0] * self.length
        self.rot2 = [0] * self.length
        self.rot3 = [0] * self.length

        self.log = open('logs/%s.txt' % datetime.datetime.now(), 'wb')
        self.time = time.time()


        self.fig, axes = plt.subplots(nrows=2, ncols=1)
        (self.ax1, self.ax2) = axes

        plt.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.9)


        self.ax1.set_ylabel('Acceleration')
        self.ax2.set_ylabel('Rotation')


        self.ax1.set_ylim([-10000,10000])
        self.ax2.set_ylim([-10000,10000])

        y = [0] * self.length

        self.accLine1 = self.ax1.plot(self.t, y, label="Acc x")[0]
        self.accLine2 = self.ax1.plot(self.t, y, label="Acc y")[0]
        self.accLine3 = self.ax1.plot(self.t, y, label="Acc z")[0]

        self.rotLine1 = self.ax2.plot(self.t, y, label="Rotation x")[0]
        self.rotLine2 = self.ax2.plot(self.t, y, label="Rotation y")[0]
        self.rotLine3 = self.ax2.plot(self.t, y, label="Rotation z")[0]

        self.ax1.legend(bbox_to_anchor = (1.0, 0.5), loc='center left', prop={'size':10})
        self.ax2.legend(bbox_to_anchor = (1.0, 0.5), loc='center left', prop={'size':10})

        device = self.getDevice()
        self.ser = serial.Serial('/dev/'+device, 9600, timeout=1)
        self.buffer = ''


    def getDevice(self):
        devices = [d for d in os.listdir('/dev/') if 'tty.usb' in d]
        if len(devices) == 0:
            print 'Error: no devices'
            return None
        if len(devices) == 1:
            return devices[0]
        print 'Choose your device'
        for num, d in enumerate(devices):
            print '%s: %s' % (num, d)
        num = input('Number:')
        return devices[num]


    def readData(self):
        '''read data from serial and save the most recent values'''

        # try:
        bytesToRead = self.ser.inWaiting()
        s = self.ser.read(bytesToRead)
        newlines = [index for index, char in enumerate(s) if char == '\n']
        # print '\t' + s
        if len(newlines) > 0:
            if len(newlines)  >= 2:
                line = s[newlines[-2]+1: newlines[-1]]
            else:
                line = self.buffer + s[:newlines[-1]]
            # print 'Line:', line
            self.buffer = s[newlines[-1]+1:]

            try:
                acc1, acc2, acc3, rot1, rot2, rot3 = map(int, line.split(','))
                now = datetime.datetime.now()
                self.log.write(now.strftime('%H:%M:%S:%f')+','+str(time.time())+','+line+'\n')
            except:
                print 'Bad line:', line
                acc1, acc2, acc3, rot1, rot2, rot3 = 0,0,0,0,0,0

            # self.acc1 = self.acc1[1:] + [acc1 - self.avg(self.acc1[-5:])]
            # self.acc2 = self.acc2[1:] + [acc2 - self.avg(self.acc1[-5:])]
            # self.acc3 = self.acc3[1:] + [acc3 - self.avg(self.acc1[-5:])]
            #
            # self.rot1 = self.rot1[1:] + [rot1 - self.avg(self.rot1[-5:])]
            # self.rot2 = self.rot2[1:] + [rot2 - self.avg(self.rot2[-5:])]
            # self.rot3 = self.rot3[1:] + [rot3 - self.avg(self.rot3[-5:])]



            self.acc1 = self.acc1[1:] + [acc1]
            self.acc2 = self.acc2[1:] + [acc2]
            self.acc3 = self.acc3[1:] + [acc3]

            self.rot1 = self.rot1[1:] + [rot1]
            self.rot2 = self.rot2[1:] + [rot2]
            self.rot3 = self.rot3[1:] + [rot3]






        else:
            self.buffer += s


    def init(self):
        '''Function for initializing the graph. Called by FuncAnimation'''

        y = [0] * self.length

        self.accLine1.set_data(self.t, y)
        self.accLine2.set_data(self.t, y)
        self.accLine3.set_data(self.t, y)

        self.rotLine1.set_data(self.t, y)
        self.rotLine2.set_data(self.t, y)
        self.rotLine3.set_data(self.t, y)


        return [self.accLine1, self.accLine2, self.accLine3, self.rotLine1,\
                self.rotLine2, self.rotLine3]


    def animate(self, i):
        '''Updates the graph. i is the frame number, which is ignored'''
        now = time.time()
        # print 'dt:', now - self.time
        self.time = now

        self.readData()

        # self.accLine1.set_ydata(self.acc1)
        # self.accLine2.set_ydata(self.acc2)
        # self.accLine3.set_ydata(self.acc3)
        #
        # self.rotLine1.set_ydata(self.rot1)
        # self.rotLine2.set_ydata(self.rot2)
        # self.rotLine3.set_ydata(self.rot3)


        self.accLine1.set_ydata(self.deriv(self.acc1))
        self.accLine2.set_ydata(self.deriv(self.acc2))
        self.accLine3.set_ydata(self.deriv(self.acc3))
        self.rotLine1.set_ydata(self.deriv(self.rot1))
        self.rotLine2.set_ydata(self.deriv(self.rot2))
        self.rotLine3.set_ydata(self.deriv(self.rot3))



        return [self.accLine1, self.accLine2, self.accLine3, self.rotLine1,\
                self.rotLine2, self.rotLine3]


    def show(self):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=1, interval=self.interval, blit=True, init_func=self.init)
        plt.show()

    def deriv(self, y):
        n = 5
        avg = float(sum(y[:n])) / n
        y2 = [x - avg for x in y[:n]]
        for index in range(n, len(y)):
            y2.append(y[index] - float(sum(y[index-n:index])) / n)
        return y2

    # def subt_avg(self, y):
    #     avg = float(sum(y)) / len(y)
    #     return [x-avg for x in y]

    def avg(self, y):
        return float(sum(y)) / len(y)

if __name__ == '__main__':
    g = Graph()
    g.show()
