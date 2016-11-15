import urllib.request
import requests
import json
import logging
import anon
import xml.etree.ElementTree as ET

class GelbooruHelper():
    def __init__(self):
        logging.info('initializing gelbooru helper')
        self.posts = None
        self.baseUrl = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index'
        self.tagUrl = '&tags='
        self.tags = ''
        self.pageUrl = '&pid='
        self.page = 0
        self.limitUrl = '&limit=5'

    def generateString(self, query):
        if query[0] == '+' or query[1] == '+':
            self.incPage()
            return self.getPostsString()
        elif query[0] == '-' or query[1] == '-':
            self.decPage()
            return self.getPostsString()
        elif query[0] == '0' or query[1] == '0':
            self.zeroPage()
            return self.getPostsString()
        elif query[1:5] == 'anon':
            return self.getAnonymizedLinksString()
        else:
            tags = query[1:]
            self.zeroPage()
            self.setTags(tags)
            return self.getPostsString()

    def getData(self):
        url = self.baseUrl + self.limitUrl + self.pageUrl + str(self.page) + self.tagUrl + self.tags
        logging.info('serving ' + url)
        data = requests.get(url).text
        tree = ET.fromstring(data)
        return tree

    def getPostsString(self):
        self.posts = self.getData()
        if not self.posts:
            self.decPage()
            logging.warning('no posts found for ' + self.tags + ' on page no.' + str(self.page))
            return('Прошу прощения, господин, я ничего не нашла на ' + str(self.page) + '-й странице ;_;')
        string = 'Страница номер ' + str(self.page) + ':\n'
        for post in self.posts:
            string += (post.attrib['file_url'] + '\n')
        return string

    def getAnonymizedLinksString(self):
        if not self.posts:
            self.posts = self.getData()
        message = 'Вот анонимизированные ссылки, господин:\n'
        for post in self.posts:
            url = 'http://noblockme.ru/api/anonymize?url=' + post.attrib['file_url']
            anonString = requests.get(url).text
            anonJson = json.loads(anonString)
            if anonJson['status'] == 0:
                anonUrl = anonJson['result']
                message += (anonUrl + '\n')
            else:
                message = 'А-а-а, не вижу страницы! Извините, господин! ;_;'
        return message

    def setTags(self, tags):
        tags = tags.replace(' ', '+')
        tags = tags.replace('&', '')
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

class DanbooruHelper():
    def __init__(self):
        logging.info('initializing danbooru helper')
        self.posts = None
        self.baseUrl = 'http://danbooru.donmai.us/posts.json'
        self.tagUrl = '&tags='
        self.tags = ''
        self.pageUrl = '&page='
        self.page = 0
        self.limitUrl = '?limit=5'

    def getData(self):
        url = self.baseUrl + self.limitUrl + self.pageUrl + str(self.page) + self.tagUrl + self.tags
        logging.info('serving ' + url)
        data = requests.get(url)
        print(data)
        print(data.text)
        datajson = json.loads(data.text)
        return datajson

    def generateString(self, query):
        if query[0] == '+' or query[1] == '+':
            self.incPage()
            return self.getPostsString()
        elif query[0] == '-' or query[1] == '-':
            self.decPage()
            return self.getPostsString()
        elif query[0] == '0' or query[1] == '0':
            self.zeroPage()
            return self.getPostsString()
        elif query[1:5] == 'anon':
            return self.getAnonymizedLinksString()
        else:
            tags = query[1:]
            self.zeroPage()
            self.setTags(tags)
            return self.getPostsString()

    def getPostsString(self):
        self.posts = self.getData()
        if not self.posts:
            self.decPage()
            logging.warning('no posts found for ' + self.tags + ' on page no.' + str(self.page))
            return('Прошу прощения, господин, я ничего не нашла на ' + str(self.page) + '-й странице ;_;')
        string = 'Страница номер ' + str(self.page) + ':\n'
        for post in self.posts:
            string += ('https://danbooru.donmai.us/posts/' + str(post['id']) + '\n')
        return string

    def getAnonymizedLinksString(self):
        if not self.posts:
            self.posts = self.getData()
        message = 'Вот анонимизированные ссылки, господин:\n'
        for post in self.posts:
            url = 'http://noblockme.ru/api/anonymize?url=' + post.attrib['file_url']
            anonString = requests.get(url).text
            anonJson = json.loads(anonString)
            if anonJson['status'] == 0:
                anonUrl = anonJson['result']
                message += (anonUrl + '\n')
            else:
                message = 'А-а-а, не вижу страницы! Извините, господин! ;_;'
        return message

    def setTags(self, tags):
        tags = tags.replace(' ', '+')
        tags = tags.replace('&', '')
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
