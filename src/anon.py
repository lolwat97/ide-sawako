import urllib.request
import json
import logging


def getAnonUrl(url):
    message = 'Вот анонимизированная ссылка, господин: '
    url = 'http://noblockme.ru/api/anonymize?url=' + url
    anonString = urllib.request.urlopen(url).read().decode('utf-8')
    anonJson = json.loads(anonString)
    message += anonJson['result']
    return message
