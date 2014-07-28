# gp_pic.py
# approximates a image using triangles
# children take the structure
# [x, y, x, y, x, y, (R, G, B)]
# the fitness test assumes a lower fitness number is better

import Image
import numpy as np
import random
import ImageDraw
import time

def load_image(filename):
    '''Opens an image file and imports it into a numpy array'''
    image = Image.open(filename)
    pixels = np.array(image)
    return pixels


def create_pop(pop_size, num_points, shape):
    '''Creates a random population of pixel arrays'''
    children = []
    for n in range(pop_size):
        child = []
        for m in range(num_points):
            pt1 = [random.randint(0,shape[0]), random.randint(0,shape[1])]
            pt2 = [random.randint(0,shape[0]), random.randint(0,shape[1])]
            pt3 = [random.randint(0,shape[0]), random.randint(0,shape[1])]
            points = pt1+pt2+pt3
            col = tuple([random.randint(0, 255) for p in range(3)])
            points.append(col)
            child.append(points)
        children.append(child)
    return children


def fitness(child_pixels, goal_pixels):
    fitness = np.sum(abs(child_pixels-goal_pixels))
    return fitness


def create_image(child, shape):
    '''creates a pixel array from a child'''
    rshape = (shape[1], shape[0])    # images use yx, not xy coordinates
    image = Image.new('RGB', rshape)
    for tri in child:
        mask = Image.new('RGB', rshape)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.polygon(tri[:6], fill=tri[-1])
        image = Image.blend(image, mask, .5)
    pixels = np.array(image)
    return pixels


def find_parents(children, goal_pixels, shape):
    return sorted(children,\
                    key=lambda c: fitness(create_image(c, shape), goal_pixels),)[:len(children)/2]


def mate_pair(mom, dad):
    n = random.randint(0, len(mom))
    child = mom[n:] + dad[:n]
    return child


def mate_pop(parents, pop_size):
    children = []
    while len(children) < pop_size:
        mom = random.choice(parents)
        dad = random.choice(parents)
        children.append(mate_pair(mom, dad))
    return children


def disp_image(child, shape):
    rshape = (shape[1], shape[0])    # images use yx, not xy coordinates
    image = Image.new('RGB', rshape)
    for tri in child:
        mask = Image.new('RGB', rshape)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.polygon(tri[:6], fill=tri[-1])
        image = Image.blend(image, mask, .5)
    image.show()


def mutate(children, mut_percent, shape):
    num_mut = int(len(children) * len(children[0]) * mut_percent)
    for n in range(num_mut):
        p = random.randint(0, len(children)-1)
        q = random.randint(0, len(children[0])-1)
        x = 2*random.randint(0, 2) # x coordinate
        y = x+1 # y coordinate
        children[p][q][x] = random.randint(0, shape[0])
        children[p][q][y] = random.randint(0, shape[1])
    return children

def run(filename):
    pop_size = 64
    num_tri = 5
    goal_pixels = load_image(filename)
    shape = goal_pixels.shape[:2]
    children = create_pop(pop_size, num_tri, shape)
    c = 0
    while True:
        c += 1
        parents = find_parents(children, goal_pixels, shape)
        if c % 6 == 0:
            print fitness(create_image(parents[0], shape), goal_pixels)
            #mparents = create_pop(pop_size, num_tri, shape)
            #parents.extend(mparents)
        if c % 64 == 0:
            disp_image(parents[0], shape)
        children = mate_pop(parents, pop_size)




if __name__ == '__main__':
    run('ocar.jpg')