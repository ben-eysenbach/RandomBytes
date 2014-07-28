# hello.py
# prints 'hello world'


import random
import sys


def fitness_test(letter_list, goal_list):
    fitness = 0
    for c in range(len(letter_list)):
        if letter_list[c] == goal_list[c]:
            fitness += 1
    return fitness


def find_parents(children, letters, goal_list):
    parents = sorted(children, key=lambda x: fitness_test(x, goal_list), reverse=True)
    return parents[:int(len(parents)/2)]



def mate_pair(mom, dad):
    n = random.randint(0,len(mom))
    return mom[:n] + dad[n:]


def mate_pop(parents, pop_size):
    children = []
    while len(children) < pop_size:
        mom = random.choice(parents)
        dad = random.choice(parents)
        children.append(mate_pair(mom, dad))
    return children


def mutate(children, letters, mut_percent):
    for n in range(mut_percent):
        p = random.randint(0,len(children)-1) # picks a child to mutate
        q = random.randint(0,len(children[p])-1) # picks a letter to mutate
        children[p][q] = random.choice(letters)
    return children


def run(goal, pop_size, mut_percent, cutoff):
    goal_list = list(goal)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
     'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
    children = [[random.choice(letters) for n in range(len(goal))] for m in range(pop_size)]
    c = 0

    while c < cutoff and goal_list not in children:
        parents = find_parents(children, letters, goal_list)
        #print ''.join(parents[0])
        children = mutate(mate_pop(parents, pop_size), letters, mut_percent)
        c += 1
    return c

def repeat_run(goal, pop_size, mut_percent, cutoff, repeats):
    c_list = []
    for n in range(repeats):
        c = run(goal, pop_size, mut_percent, cutoff)
        c_list.append(c)
    avg = sum(c_list) / len(c_list)
    return avg

if __name__ == '__main__':
    c = run('hello world', 100, 10, 1000)
    print "Converged in %d generations" % c