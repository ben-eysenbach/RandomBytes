# implementation of a car class
# todo change to t**2
# add delete object method incorporating delete graphic function
import time

def safe_dist(velocity):
    '''Calculates the same following distance'''
    return 2 * velocity + 5


class Car:

    def __init__(self, canvas, color='white', position=0, velocity=0, v_max=27, a_max=4, a_min=-8): ##
        self.canvas = canvas
        self.color = color
        self.graphic = self.canvas.create_rectangle(0, 100, 20, 110, fill=self.color) # rect from setup was renamed graphic
		
        self.position = position
        self.velocity = velocity
        self.v_max = v_max
        self.a_max = a_max
        self.a_min = a_min  # this will be negative because it's deceleration
        self.acceleration = 0

    def accelerate(self, proximity, k=1):
        '''Calculates the acceleration or deceleration of a car given its
        proximity to the car in front of it.
        k is the "jerkiness" factor'''
        if proximity == -1:
            self.acceleration = self.a_max
        else:
            self.acceleration = k * (proximity - safe_dist(self.velocity))

    def validate(self):
        '''confirms that the acceleration and velocity are less than the
        maximums, and adjusts then if they aren\'t'''
        if self.acceleration > self.a_max:
            self.acceleration = self.a_max
        elif self.acceleration < self.a_min:
            self.acceleration = self.a_min
        if self.velocity + self.acceleration > self.v_max:
            self.acceleration = 0
        if self.velocity < 0:
            self.velocity = 0

    def move(self, delta_time)	:
        '''changes the position of the car'''
        self.position += self.velocity * delta_time + 0.5 * self.acceleration * delta_time
        self.canvas.coords(self.graphic, self.position, 100, self.position + 20, 110) ##
        self.velocity += self.acceleration * delta_time

    def delete_graphic(self):
        '''delete the rectangle graphic so that they dont pile up at the line
        which I believe happens because the Car object is released but the tk graphic
        element hangs around. remove this and where its called to see what I mean.''' 
        self.canvas.delete(self.graphic)
		
class Stoplight:

    def __init__(self, canvas):
        self.canvas = canvas
        self.status = 1  # 1 for green, 0 for red
        self.start_time = time.time()
        self.duration = 5
        self.graphic = self.canvas.create_rectangle(0, 0, 40, 40, fill="green")	

    def check(self):
        if time.time()-self.start_time > self.duration:
            self.start_time = time.time()
            self.status = self.status ^ 1
            if self.status == 1:
	            self.canvas.itemconfig(self.graphic, fill="green")
            else:
	            self.canvas.itemconfig(self.graphic, fill="red")
