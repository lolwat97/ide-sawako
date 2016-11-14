from pybooru import Pybooru
import urllib.request
import xml.etree.ElementTree as ET

class GelbooruHelper():
    def __init__(self):
        self.baseUrl = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index'
        self.tagUrl = '&tags='
        self.tags = ''
        self.pageUrl = '&pid='
        self.page = 0
        self.limitUrl = '&limit=10'

    def getData(self):
        url = self.baseUrl + self.tagUrl + self.tags + self.limitUrl + self.pageUrl + str(self.page)
        print('INFO     got request for ' + url)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        tree = ET.fromstring(data)
        return tree

    def getPostsString(self):
        posts = self.getData()
        if not posts:
            self.decPage()
            return('Прошу прощения, господин, я ничего не нашла на ' + str(self.page) + '-й странице ;_;')
        string = 'Page ' + str(self.page) + ':\n'
        for post in posts:
            string += (post.attrib['file_url'] + '\n')
        return string

    def setTags(self, tags):
        tags = tags.replace(' ', '+')
        self.tags = tags

    def zeroPage(self):
        self.page = 0

    def incPage(self):
        self.page += 1

    def decPage(self):
        if self.page > 0:
            self.page -= 1
