import sleekxmpp
import cleverbot

import json
import time
import re
import random

from talking import Talking
from cleverbot_text_modification import TextModifier


class Bot(sleekxmpp.ClientXMPP):
    def __init__(self, configFile, phrasesFile, namesFile, otherFile):
        config = self.load_config(configFile)

        self.cleverbotInstance = cleverbot.Cleverbot()

        sleekxmpp.ClientXMPP.__init__(self, config['jid'], config['pass'])
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC

        self.room = config['room']
        self.nick = config['nick']

        self.talk = Talking(phrasesFile)
        self.modifier = TextModifier(self.nick, namesFile, otherFile)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)

    def load_config(self, configFile):
        configJson = open(configFile)
        config = json.load(configJson)
        print('INFO     loaded config')
        return config

    def start(self, event):
        self.get_roster()
        print('INFO     got roster')
        self.send_presence()
        print('INFO     presence sent')
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        wait=True)
        print('INFO     joined ' + self.room)

    def easy_message(self, msg):
        self.send_message(mto = self.room,
                          mbody = msg,
                          mtype = 'groupchat')

    def muc_message(self, msg):
        if msg['mucnick'] != self.nick:

            if self.nick.lower() == msg['body'][:3].lower():
                self.easy_message(msg['mucnick']+': ' + self.modifier.modify(self.cleverbotInstance.ask(msg['body'][4:])))

            if self.talk.check_chat_greeting(msg['body']):
                self.easy_message(self.talk.random_greeting(msg['mucnick']))

            if self.talk.check_goodbye(msg['body']) or self.talk.check_sleep(msg['body']):
                self.easy_message(self.talk.random_goodbye(msg['mucnick']))

            if self.talk.check_swear(msg['body']) and self.nick in msg['body']:
                self.easy_message(self.talk.random_swear())

            if msg['mucnick'] == 'ara~ara' and msg['body'][0] == '!':
                if random.random() >= 0.2:
                    self.easy_message('! ' + self.cleverbotInstance.ask(msg['body']))
                else:
                    self.easy_message(self.talk.talk_with_ara_end())

            if msg['body'][0] == '#':
                try:
                    to_reg = msg['body'][1:]
                    to_val = re.search('(\d+.?\d*[ +*/-^]*)+', to_reg).group(0)
                    if any(x in to_val for x in ['**', '<<', '>>', '^', '[', ']']):
                        self.easy_message('Ууу, сложно. %s, дай чего попроще!' % msg['mucnick'])
                        return 0
                    val = eval(to_val)
                    self.easy_message(self.talk.random_ithink(str(val)))
                except: pass
