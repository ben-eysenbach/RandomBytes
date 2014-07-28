#! /usr/bin/python

# Uncomment if you want to place in /usr/local/bin (so you could query $what is ...?!)
# import sys
# sys.path.append('')


from wiki_abstract import *

if len(sys.argv) < 3:
    print '\nUsage: What is [whatever]\n'
else:
    print '\n'
    print get_abs(' '.join([t.strip('?') for t in sys.argv[2:] if t not in ['a', 'the']]))
    print '\n'
