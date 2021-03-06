import six.moves.urllib as urllib
import six
import re
import webbrowser
import xmltodict
from lxml import html


def extract_download_link(link):
    start = link.find('url/') + 4
    return link[start:]


show_name = six.moves.input("TV Show name: ")
download_server = six.moves.input("Download from (Eg. mega) :")
url = "http://awesomedl.ru/?" + urllib.parse.urlencode({'feed': 'rss2', 's': 'House of Cards'})
searchpage = urllib.request.urlopen(url).read()
result = xmltodict.parse(searchpage)
finalstr = []
if 'rss' in result and 'channel' in result['rss'] and 'item' in result['rss']['channel']:
    for episode in result['rss']['channel']['item']:
        epilinks = html.fromstring(episode['content:encoded'])
        links = []
        for downlink in epilinks.xpath("//a"):
            if str(downlink.text).lower() == download_server:
                links.append(extract_download_link(downlink.get("href")));
        finalstr.append({'title': episode['title'], 'link': links})
    [webbrowser.open(url, 0, True) for url in finalstr[0]['link']]
else:
    print('No result found')
exit()
