## wiki_abstract_race.py


## Part 1
## converts html document into file
## format: [page, [link1, link2, ...]]
import re

def parse(piece):
    if '</title>' not in piece:
        return
    [title, data] = piece.split('</title>')
    links = re.findall('(?<=<anchor>)[\w+\s*]+', data)
    if 'External links' in links:
        links.remove('External links')
    if 'See also' in links:
        links.remove('See also')
    if 'Notes and references' in links:
        links.remove('Notes and references')
    if 'Further reading' in links:
        links.remove('Further reading')
    if 'References' in links:
        links.remove('References')
    if 'Notes' in links:
        links.remove('Notes')
    if len(links) == 0:
        return
    return title, links

f = open('/home/bce/Documents/Python/wikipedia_abstracts/enwiki-latest-abstract.xml.1')
s = open('/home/bce/Documents/Python/wikipedia_abstracts/save.txt', 'w')
pieces = ['']
while f.read(10000) and len(pieces) < 10:
    temp = f.read(10000).split('<title>Wikipedia: ')
    pieces[-1] += temp[0]
    for t in temp[1:]:
        pieces.append(t)
    
for p in pieces:
    print parse(p)
    if parse(p):
        s.write(parse(p))
    raw_input()
    print
