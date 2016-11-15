import requests
from lxml.html import fromstring

def getPageTitle(url):
    request = requests.get(url)
    tree = fromstring(request.content)
    title = tree.findtext('.//title')
    return title
