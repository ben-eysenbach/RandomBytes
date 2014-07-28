#lint:disable
# tests to see if the car will crash in various scenarios

from car import *
from Tkinter import *
import time
import random

# main file

def test():
    master = Tk()
    w = Canvas(master, width=400, height=200)
    w.pack()
    w.create_line(390,75,390,125)
    h = w.create_rectangle(50, 100, 60, 105, fill="red")
    a = w.create_rectangle(0, 100, 10, 105, fill="blue")
    f = w.create_rectangle(-100, 100, -90, 105, fill="yellow")
    l = w.create_rectangle(0, 0, 20, 20, fill="green")
    fer = Car(-100, 1, 50, 6, -8)
    honda = Car(50, 1, 27, 4, -8)
    audi = Car(0, 1, 30, 10, -8)

    light = Stoplight()
    while fer.position < 400:
        time.sleep(.03)
        if light.status == 0:
            honda.accelerate(380-honda.position, 1)
        else:
            honda.accelerate(-1, 1)
        if light.status == 0 and 380-audi.position < honda.position-audi.position:
            audi.accelerate(380-audi.position)
        else:
            audi.accelerate(honda.position-audi.position-10, 5)
        if light.status == 0 and 380-fer.position < audi.position - fer.position:
            fer.accelerate(380-fer.position)
        else:
            fer.accelerate(audi.position-fer.position-10, 5)
        if honda.position > 380:
            honda.position = 500
            honda.velocity = 0

        if audi.position > 380:
            audi.position = 500
            audi.velocity = 0

        honda.validate()
        audi.validate()
        fer.validate()
        honda.move(.1)
        audi.move(.1)
        fer.move(.1)
        w.coords(h, int(honda.position), 100, int(honda.position)+10, 105)
        w.coords(a, int(audi.position), 100, int(audi.position)+10, 105)
        w.coords(f, int(fer.position), 100, int(fer.position)+10, 105)
        master.update()
        light.check()
        if light.status == 1:
            w.itemconfig(l, fill="green")
        else:
            w.itemconfig(l, fill="red")
    master.mainloop()

def setup():
    master = Tk()
    w = Canvas(master, width=800, height=200)
    w.pack()
    w.create_line(790,75,790,125)
    
    carlist = [Car(w)] 
    light = Stoplight(w)
    color_palette = ['yellow', 'blue', 0]
    
	
    while len(carlist) < 20:
        time.sleep(.05)
        number_of_cars = len(carlist)

        if number_of_cars < 10 and random.random() < .01:	# random qualifier satisfied very infrequently, 1/100(?)
            c = color_palette[color_palette[2]] ; color_palette[2] ^= 1 	# alternates the colors of the cars, clever bitshift
            carlist.append(Car(w, c, 0, 20, random.randint(15,30), random.randint(5, 10))) ##
		
        if number_of_cars > 0:
            if light.status == 1:
                carlist[0].accelerate(-1)
            else:
                carlist[0].accelerate(770-carlist[0].position)
        
        # deals with what happense near the stoplight, and with proximity to other cars everywhere
        for car_count in range(1,number_of_cars): # so, for all cars except the first created
            pos = carlist[car_count].position
            prox = carlist[car_count - 1].position - pos
            if light.status == 0 and 770 - pos < prox:	# i.e., if it's closer to the light than the car in front of it
                carlist[car_count].accelerate(770-pos)
            else:
                carlist[car_count].accelerate(carlist[car_count-1].position - carlist[car_count].position - 20)

        for car in carlist: 
            car.validate()
            car.move(.1)


        print '-'*50, '\n'

        for car in carlist:
            print "number_of_cars: %.2f" % number_of_cars
            print "Position: %.2f" % car.position
            print "Velocity: %.2f" % car.velocity
            print "Acceleration: %.2f" % car.acceleration

        #for car_count in range(0, number_of_cars):
        #    print "Position: %.2f" % carlist[car_count].position
        #    if car_count != 0: 
        #        print "Prox: %.2f" % carlist[car_count-1].position - carlist[car_count].position
        #    print "Velocity: %.2f" % car.velocity
        #    print "Acceleration: %.2f" % car.acceleration

        if carlist[0].position > 770:
            carlist[0].delete_graphic() # removing the reference to a Car in carlist does not remove
										# the tk rectangle graphic, so added this kludge method.
										# Maybe later on, whence we understand Python memory management
										# better, we can fix it.
            carlist = carlist[1:] 	
									
        light.check()

        master.update()
    master.mainloop()

if __name__ == '__main__':
    setup()
