
class Card:
    
    def __init__(self, name, desc, type):
        self._name = name
        self._desc = desc
        self._type = type

    def __str__(self):
        return self._name
    
    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def type(self):
        return self._type   