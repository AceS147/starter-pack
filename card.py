

class Card:
    
    def __init__(self, name, desc, type):
        self.name = name
        self.desc = desc
        self.type = type

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