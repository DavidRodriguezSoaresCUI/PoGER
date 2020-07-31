
class Variable:

    def __init__(self, value):
        assert type(value) in [int, float, bool]
        self.value = value

    def assign(self, new_value):
        self.value = new_value

    def __add__(self, other):
        return self.value + other

    def __iadd__(self, other):
        self.value += other
        #return self

    def __sub__(self, other):
        return self.value - other

    def __isub__(self, other):
        self.value -= other
        #return self

    def __mul__(self, other):
        return self.value * other

    def __imul__(self, other):
        self.value *= other
        #return self

    def __div__(self, other):
        return self.value / other

    def __idiv__(self, other):
        self.value /= other
        #return self
        

class Instruction:

    def __init__(self):
        pass
        

    

