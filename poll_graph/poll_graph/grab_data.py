import requests
import re


def get_data_list():
    xml = requests.get('http://www.beijingaqifeed.com/BeijingAQI/BeijingAir.xml')
    ascii_xml = xml.text.encode('ascii', 'ignore') #xml.text method is part of requests library
    data = re.findall('(?<=!\[CDATA\[).*(?=\]\])', ascii_xml)
    split_data = [time.split('; ') for time in data]
    pretty_data = [[time[0], time[3]] for time in split_data if len(time) > 3]
    now = pretty_data[0][1] # this is a string
    print now
    good_data = []
    for entry in pretty_data:
        aqi = entry[1]
        date = entry[0].split(' ')[0]
        hour = entry[0].split(' ')[1].split(':')[0]
        year = date.split('-')[2]
        month = date.split('-')[0]
        day = date.split('-')[1]
        date_str = '[{v: new Date(%s, %s, %s, %s), f: "%d:00"}, %s]' % (year, month, day, hour, int(hour), aqi)
        good_data.append(date_str)
    return [good_data, now]
    
if __name__ == '__main__':
    get_data_list()
