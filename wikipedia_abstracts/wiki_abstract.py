## wiki_abstract.py
## returns wikipedia abstracts
## wiki json format: load['query']['pages']['8983183']['revisions'][0]['*']

import urllib2, json, re

def make_link(subj):
    '''creates a url'''
    return 'http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content&rvsection=0&redirects' % subj.replace(' ', '%20')

def json_to_text(json_load):
    '''extracts the text from json'''
    page_id = json_load['query']['pages'].keys()[0]
    try:
        return json_load['query']['pages'][page_id]['revisions'][0]['*'].encode('utf-8')
    except KeyError:
        raise KeyError

def parse(text):
    '''Formats wikipedia text by removing links and styling'''
    text = re.sub(r'\<ref.*?\</ref\>', '', text)        #removes spanning ref tags
    text = re.sub(r'\<.*?\>', '', text)                 #removes individual tags ex <ref />
    text = re.sub(r'\{\{[^{{]*?\}\}', '', text)         #removes {{qwerty}}
    text = re.sub(r'\{\{[^{{]*?\}\}', '', text)         #repeated to removed embedded {{}}
    text = re.sub(r'\{\{[^{{]*?\}\}', '', text)
    
    
    text = re.sub(r'\[\[(?P<tag>[^|]*?)\]\]', '\g<tag>', text)      #replaces [[tag]] with tag if | not in tag
    text = re.sub(r'\[\[(File|Image).*?\[\[.*?\]\].*?\]\]', '', text)       #removes [[File/Image...[[...]]...]]
    text = re.sub(r'\[\[(File|Image).*?\]\]', '', text)             #removes [[Files/Image...]]
    text = re.sub(r'\[\[.*?\|(?P<tag2>.*?)\]\]', '\g<tag2>', text)  #replaces [[link|text]] with text
    text = text.replace('\'\'\'', '')                   #removes '''
    text = text.replace('&nbsp;', ' ')                  #removes no break spaces  
    return text.strip()

def get_abs(subj):
    '''fetches json object from wikipedia'''
    req = urllib2.Request(make_link(subj), None, {'User-Agent':'wiki_scraper.py'})
    data = urllib2.urlopen(req).read()
    try:
        load = json.loads(data)
        return parse(json_to_text(load))
    except KeyError:
        return 'The Knowledge you requested is unknown to Mankind.'

