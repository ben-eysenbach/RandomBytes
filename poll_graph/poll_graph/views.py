from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from grab_data import get_data_list

import os

def graph(request):
    t = get_template('template.html')
    data = get_data_list() #returns data_list and current reading
    c = Context({'mydata': data[0], 'now' : data[1]})
    html = t.render(c)
    return HttpResponse(html)
    
def about(request):
    t = get_template('about')
    c = Context({})
    html = t.render(c)
    return HttpResponse(html)
