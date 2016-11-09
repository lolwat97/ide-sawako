import json

class NameModifier():
    def __init__(self, name, namesFile):
        self.name = name
        self.names = self.load_names(namesFile)

    def load_names(self, namesFile):
        namesJson = open(namesFile)
        names = json.load(namesJson)
        print('INFO     loaded names for name translation')
        return names

    def modify(self, str):
        modified = str
        for x in self.names['names']:
            modified = modified.replace(' ' + x, ' ' + self.name)
            modified = modified.replace(' ' + x.lower(), ' ' + self.name)
            modified = modified.replace(x + ' ', self.name + ' ')
            modified = modified.replace(x.lower() + ' ', self.name + ' ')
        return modified

class OtherModifier():
    def __init__(self, otherFile):
        self.other = self.load_other(otherFile)

    def load_other(self, otherFile):
        otherJson = open(otherFile)
        other = json.load(otherJson)
        print('INFO     loaded other substitutions')
        return other

    def modify(self, str):
        modified = str
        for x in self.other:
            modified = modified.replace(x, self.other[x])
            modified = modified.replace(x.lower(), self.other[x].lower())
        return modified

class TextModifier():
    def __init__(self, name, namesFile, otherFile):
        self.nameModifier = NameModifier(name, namesFile)
        self.otherModifier = OtherModifier(otherFile)

    def modify(self, str):
        modified = str
        modified = self.nameModifier.modify(modified)
        modified = self.otherModifier.modify(modified)
        return modified
