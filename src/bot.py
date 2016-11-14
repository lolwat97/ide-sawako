import sleekxmpp
import cleverbot

import json
import time
import re
import random
import logging

from talking import Talking
from cleverbot_text_modification import TextModifier
from booru import GelbooruHelper


class Bot(sleekxmpp.ClientXMPP):
    def __init__(self, configFile, phrasesFile, namesFile, otherFile):

        logging.basicConfig(level = logging.INFO,
                            format = '%(levelname)-8s %(message)s')

        config = self.load_config(configFile)

        self.cleverbotInstance = cleverbot.Cleverbot()
        self.gelbooruHelper = GelbooruHelper()

        sleekxmpp.ClientXMPP.__init__(self, config['jid'], config['pass'])
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC

        self.room = config['room']
        self.nick = config['nick']

        self.talk = Talking(phrasesFile)
        self.modifier = TextModifier(self.nick, namesFile, otherFile)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message_handler)

    def load_config(self, configFile):
        configJson = open(configFile)
        config = json.load(configJson)
        logging.info('loaded config')
        return config

    def start(self, event):
        self.get_roster()
        logging.info('got roster')
        self.send_presence()
        logging.info('presence sent')
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        wait=True)
        logging.info('joined ' + self.room)

    def message_muc(self, msg):
        self.send_message(mto = self.room,
                          mbody = msg,
                          mtype = 'groupchat')

    def message_handler(self, msg):
        if msg['mucnick']:
            logging.info('got muc message')
            self.muc_message_handler(msg)
        else:
            logging.info('got private message')
            self.pm_message_handler(msg)

    def pm_message_handler(self, msg):
        if msg['body'][0] == '$':
            if msg['body'][1] == '+':
                self.gelbooruHelper.incPage()
                msg.reply(self.gelbooruHelper.getPostsString()).send()
            elif msg['body'][1] == '-':
                self.gelbooruHelper.decPage()
                msg.reply(self.gelbooruHelper.getPostsString()).send()
            elif msg['body'][1] == '0':
                self.gelbooruHelper.zeroPage()
                msg.reply(self.gelbooruHelper.getPostsString()).send()
            else:
                tags = msg['body'][1:]
                self.gelbooruHelper.zeroPage()
                self.gelbooruHelper.setTags(tags)
                msg.reply(self.gelbooruHelper.getPostsString()).send()
        elif msg['body'][0] == '#':
            try:
                to_reg = msg['body'][1:]
                to_val = re.search('(\d+.?\d*[ +*/-^]*)+', to_reg).group(0)
                if any(x in to_val for x in ['**', '<<', '>>', '^', '[', ']']):
                    msg.reply('Ууу, сложно, дай чего попроще!').send()
                    return 0
                val = eval(to_val)
                self.reply(self.talk.random_ithink(str(val))).send()
            except: pass
        else:
            msg.reply(self.modifier.modify(self.cleverbotInstance.ask(msg['body']))).send()

    def muc_message_handler(self, msg):
        if msg['mucnick'] != self.nick:

            if self.nick.lower() == msg['body'][:3].lower():
                self.message_muc(msg['mucnick']+': ' + self.modifier.modify(self.cleverbotInstance.ask(msg['body'][4:])))

            if self.talk.check_chat_greeting(msg['body']):
                self.message_muc(self.talk.random_greeting(msg['mucnick']))

            if self.talk.check_goodbye(msg['body']) or self.talk.check_sleep(msg['body']):
                self.message_muc(self.talk.random_goodbye(msg['mucnick']))

            if self.talk.check_swear(msg['body']) and self.nick in msg['body']:
                self.message_muc(self.talk.random_swear())

            if msg['mucnick'] == 'ara~ara' and msg['body'][0] == '!':
                if random.random() >= 0.2:
                    self.message_muc('! ' + self.cleverbotInstance.ask(msg['body']))
                else:
                    self.message_muc(self.talk.talk_with_ara_end())

            if msg['body'][0] == '$':
                if msg['body'][1] == '+':
                    self.gelbooruHelper.incPage()
                    self.message_muc(self.gelbooruHelper.getPostsString())
                elif msg['body'][1] == '-':
                    self.gelbooruHelper.decPage()
                    self.message_muc(self.gelbooruHelper.getPostsString())
                elif msg['body'][1] == '0':
                    self.gelbooruHelper.zeroPage()
                    self.message_muc(self.gelbooruHelper.getPostsString())
                else:
                    tags = msg['body'][1:]
                    self.gelbooruHelper.zeroPage()
                    self.gelbooruHelper.setTags(tags)
                    self.message_muc(self.gelbooruHelper.getPostsString())

            if msg['body'][0] == '#':
                try:
                    to_reg = msg['body'][1:]
                    to_val = re.search('(\d+.?\d*[ +*/-^]*)+', to_reg).group(0)
                    if any(x in to_val for x in ['**', '<<', '>>', '^', '[', ']']):
                        self.message_muc('Ууу, сложно. %s, дай чего попроще!' % msg['mucnick'])
                        return 0
                    val = eval(to_val)
                    self.message_muc(self.talk.random_ithink(str(val)))
                except: pass
