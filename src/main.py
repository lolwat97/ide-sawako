from bot import Bot
import logging

floodchatBot = Bot('json/config_floodchat.json')
shinkaiBot = Bot('json/config_shinkai.json')
umeBot = Bot('json/config_ume.json')
lastBot = Bot('json/config_last.json')

if(floodchatBot.connect()):
    floodchatBot.process(block = False)
if(shinkaiBot.connect()):
    shinkaiBot.process(block = False)
if(umeBot.connect()):
    umeBot.process(block = False)
