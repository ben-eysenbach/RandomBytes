## keyterms.py
## takes a list of keyterms and outputs their wikipedia abstracts
## note: the input list should be raw ascii with each term on a new line

from wiki_abstract import *

def open_files(location):
    to_read = open(location, 'r')
    to_write = open('extended_'+location, 'w')
    return to_read, to_write
    
def write_keyterms((to_read, to_write)):
    terms = [t.strip().capitalize() for t in to_read.readlines()]
    for t in terms:
        print 'Getting: ' + t
        try:
            data = t + ':\n\n' + get_abs(t) + '\n\n\n'
            to_write.write(data)
        except:
            print 'Error'


location = 'keyterms.txt'
write_keyterms(open_files(location))
