## wiki_races2.py
## revisions: 
##     makes use of the wikipedia api for faster retreival(uses pllinks flag)
## note: the wikipedia api limits bots to 500 links
## therefore, the path may not be the fastest, but the program should run faster anyway


import urllib2
import re
import sys
import random

def make_url(title):
    '''converts a string into a wikipedia url'''
    # make sure to use format=xml
    title = title.strip('[]')
    return 'http://en.wikipedia.org/w/api.php?format=xml&action=query&rvprop=content&prop=revisions&prop=links&pllimit=500&titles=' + title.replace(' ', '%20')

def find_links(title):
    '''returns the titles of pages mantioned on this page'''
    
    print "Finding links for", title
    f = urllib2.urlopen(make_url(title), timeout = 1)
    text = f.read()
    return re.findall('(?<=title=\")\w+\s*\w+', text)

        
def unsearched(d):
    print "Running unsearched"
    titles = []
    for k in d.values():
        for v in k:
            if v not in d.keys():
                titles.append(v)
    if len(titles) == 0:
        raise "Dead End"
    #otherwise results are skewed towards begining of alphabet
    random.shuffle(titles) 
    return titles

start = raw_input("Starting page: ")
end = raw_input("Destination: ")
links = {start: find_links(start)}
to_search = []
while end not in links.values():
    if len(to_search) == 0:
        try:
            to_search = unsearched(links)
        except "Dead End":
            print "Dead end. Sorry"
            print "Exiting..."
            sys.exit()
    if to_search[-1] in links.keys():
        to_search.pop()
    else:
        try:
            links[to_search[-1]] = find_links(to_search[-1])
        except urllib2.URLError:
            print "Timeout"
        except urllib2.socket.timeout:
            print "Timeout"
        except urllib2.socket.error:
            print "Timeout"
        to_search.pop()
print "Done"
