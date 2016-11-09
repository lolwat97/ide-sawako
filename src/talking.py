import random
import json

class Talking():

    def __init__(self, phrasesFile):
        self.phrases = self.load_phrases(phrasesFile)

    def load_phrases(self, phrasesFile):
        phrasesJson = open(phrasesFile)
        phrases = json.load(phrasesJson)
        print('INFO     loaded phrases')
        return phrases

    def check_greeting(self, msg):
        if (any(x in msg.lower() for x in self.phrases['greets_chat'])):
            return True
        else:
            return False

    def check_chat_greeting(self, msg):
        if (self.check_greeting(msg) and (any(x in msg.lower() for x in self.phrases['shinkai_names']))):
            return True
        else:
            return False

    def check_goodbye(self, msg):
        if (any(x in msg.lower() for x in self.phrases['goodbyes_chat'])) and (any(x in msg.lower() for x in self.phrases['shinkai_names'])):
            return True
        else:
            return False

    def check_sleep(self, msg):
        if (any(x in msg.lower() for x in self.phrases['sleep_chat'])) and (any(x in msg.lower() for x in self.phrases['shinkai_names'])):
            return True
        else:
            return False

    def check_swear(self, msg):
        if (any(x in msg.lower() for x in self.phrases['swear_chat'])):
            return True
        else:
            return False

    def random_reaction(self):
        return random.choice(self.phrases['reactions'])

    def random_greeting(self, name):
        return random.choice(self.phrases['greets_bot']) % name

    def random_goodbye(self, name):
        return random.choice(self.phrases['goodbyes_bot']) % name

    def random_swear(self):
        return random.choice(self.phrases['swear_bot'])

    def random_ithink(self, str):
        return random.choice(self.phrases['ithink']) % str

    def talk_with_ara_end(self):
        return random.choice(self.phrases['with_ara_end'])
