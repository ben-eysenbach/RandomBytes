import urllib2
import re

def url_convert(string):
    string = string.strip('[]')
    return 'http://en.wikipedia.org/w/api.php?action=query&rvprop=content&prop=revisions&prop=links&pllimit=500&titles=water' + string.replace(' ', '%20')
        
f = open('wikipedia_dict.txt', 'r+')

start = raw_input('What is the starting point: ')
end = raw_input('What is the end point: ')

network = [(start,[])]
sites = [] #list of entries in network
current_sites = [start]
counter = 0 #source of current_sites list from network
solved = False
solution = []
while solved == False:
    for site in current_sites:
        if solved == True:
            break
        if site not in sites:
            links = [] #links from the site
            website = urllib2.urlopen(url_convert(site))
            website = website.read()
            match = re.findall(r'\[\[\w*]]', website)
            for entry in match:
                entry = entry.strip('[]')
                links.append(entry)
                if entry.lower() == end.lower():
                    solution = [end, site]
                    solved = True
                    break
            network.append((site,links))
            print network[-1] # only prints the last entry
            print '\n'

    sites = []
    for entry in network:
        sites.append(entry[0])

    current_sites = network[counter][1]
    counter += 1


counter = 2
while solution[-1] not in network[1][1]:
    if solution[-1] in network[counter][1]:
        solution.append(network[counter][0])
        counter = 2
    else:
        coutner += 1

solution.append(start)

print "Here's you map:"
print solution
    

