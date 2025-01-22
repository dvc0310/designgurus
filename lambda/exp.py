import re

# type var = string
# type exp = Var of var | Lam of var * exp | App of exp * exp

class Var:
    def __init__(self, var):
        self.var = var

    def __eq__(self, other):
        return isinstance(other, Var) and self.var == other.var

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return f"Var({self.var})"
    
    def __hash__(self):
        return hash(self.var)


class Lam:
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp

    def __eq__(self, other):
        return isinstance(other, Lam) and self.var == other.var and self.exp == other.exp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Lam({self.var}, {self.exp})"

    def __hash__(self):
        return hash((self.var, self.exp))


class App:
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def __eq__(self, other):
        return isinstance(other, App) and self.exp1 == other.exp1 and self.exp2 == other.exp2

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"App({self.exp1}, {self.exp2})"
    
    def __hash__(self):
        return hash((self.exp1, self.exp2))