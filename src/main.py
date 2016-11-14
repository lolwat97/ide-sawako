from bot import Bot
import logging

floodchatBot = Bot('json/config_floodchat.json', 'json/phrases.json', 'json/names.json', 'json/other.json')
shinkaiBot = Bot('json/config_shinkai.json', 'json/phrases.json', 'json/names.json', 'json/other.json')
umeBot = Bot('json/config_ume.json', 'json/phrases.json', 'json/names.json', 'json/other.json')

if(floodchatBot.connect()):
    floodchatBot.process(block = False)
if(shinkaiBot.connect()):
    shinkaiBot.process(block = False)
if(umeBot.connect()):
    umeBot.process(block = False)
