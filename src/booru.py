from pybooru import Pybooru
import urllib.request
import logging
import xml.etree.ElementTree as ET

class GelbooruHelper():
    def __init__(self):
        logging.info('initiating gelbooru helper')
        self.baseUrl = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index'
        self.tagUrl = '&tags='
        self.tags = ''
        self.pageUrl = '&pid='
        self.page = 0
        self.limitUrl = '&limit=5'

    def getData(self):
        url = self.baseUrl + self.tagUrl + self.tags + self.limitUrl + self.pageUrl + str(self.page)
        logging.info('serving ' + url)
        data = urllib.request.urlopen(url).read().decode('utf-8')
        tree = ET.fromstring(data)
        return tree

    def getPostsString(self):
        posts = self.getData()
        if not posts:
            self.decPage()
            logging.warning('no posts found for ' + self.tags + ' on page no.' + str(self.page))
            return('Прошу прощения, господин, я ничего не нашла на ' + str(self.page) + '-й странице ;_;')
        string = 'Page ' + str(self.page) + ':\n'
        for post in posts:
            string += (post.attrib['file_url'] + '\n')
        return string

    def setTags(self, tags):
        tags = tags.replace(' ', '+')
        logging.debug('setting tags ' + tags)
        self.tags = tags

    def zeroPage(self):
        logging.debug('zeroing page')
        self.page = 0

    def incPage(self):
        self.page += 1
        logging.debug('incrementing page to ' + str(self.page))

    def decPage(self):
        if self.page > 0:
            self.page -= 1
            logging.debug('decrementing page to ' + str(self.page))
