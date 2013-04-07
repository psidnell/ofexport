class TypeOf(object):
    def __init__(self, name, thetype):
        self.thetype = thetype
        self.name = name
    def __get__(self, instance, owner):
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        return None
    def __set__(self, instance, value):
        if value != None:
            assert isinstance (value, self.thetype), self.name + ': expected type ' + str(self.thetype) + ' got ' + str (value.__class__)
        instance.__dict__[self.name] = value