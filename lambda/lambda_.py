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


# (* generates a fresh variable name *)
def newvar():
    x = 0

    def generate():
        nonlocal x
        c = x
        x += 1
        return "z" + str(c)

    return generate


newvar_gen = newvar()


# (* computes the free (non-bound) variables in e *)
def fvs(e):
    if isinstance(e, Var):
        return [e.var]
    elif isinstance(e, Lam):
        return [y for y in fvs(e.exp) if y != e.var]
    elif isinstance(e, App):
        return fvs(e.exp1) + fvs(e.exp2)
    else:
        raise TypeError("Invalid expression type")



# (* substitution: subst e y m means
#    "substitute occurrences of variable y with m in the expression e" *)
def subst(e, y, m):
    if isinstance(e, Var):
        if y == e.var:
            return m
        else:
            return e
    elif isinstance(e, App):
        return App(subst(e.exp1, y, m), subst(e.exp2, y, m))
    elif isinstance(e, Lam):
        if y == e.var:
            return Lam(e.var, e.exp)
        elif not any(x == e.var for x in fvs(m)):
            return Lam(e.var, subst(e.exp, y, m))
        else:
            z = newvar_gen()
            e_prime = subst(e.exp, e.var, Var(z))
            return Lam(z, subst(e_prime, y, m))
    else:
        raise TypeError("Invalid expression type")






# (* beta reduction. *)
def reduce(e):
    if isinstance(e, App):
        if isinstance(e.exp1, Lam):
            return subst(e.exp1.exp, e.exp1.var, e.exp2)
        else:
            e1_prime = reduce(e.exp1)
            if e1_prime != e.exp1:
                return App(e1_prime, e.exp2)
            else:
                return App(e.exp1, reduce(e.exp2))
    elif isinstance(e, Lam):
        return Lam(e.var, reduce(e.exp))
    else:
        return e




def reduce_multi(x):
    old1 = x
    new1 = reduce(x)
    if old1 == new1:
        return old1
    else:
        return reduce_multi(new1)