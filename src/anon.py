import urllib.request
import requests
import json
import logging

def getAnonUrl(url):
    url = 'http://noblockme.ru/api/anonymize?url=' + url
    anonString = requests.get(url).text
    anonJson = json.loads(anonString)
    if anonJson['status'] == 0:
        message = 'Анонимизировано, господин: ' + anonJson['result']
    else:
        message = 'А-а-а, не вижу страницы! Извините, господин! ;_;'
    return message
