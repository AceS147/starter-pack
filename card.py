

class Card:
    
    def __init__(self, name, desc, type_):
        self._name = name
        self._desc = desc
        self._type = type_

    def __str__(self):
        return self.name
    
    @property
    def name(self):
        return self.name

    @property
    def desc(self):
        return self.desc

    @property
    def type(self):
        return self.type   