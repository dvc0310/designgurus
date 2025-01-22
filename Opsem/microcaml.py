# microcaml.py

from enum import Enum, auto
from typing import Any, List, Tuple, Union, Optional


# --------------------------
# 1. Exceptions
# --------------------------

class TypeError(Exception):
    """Raised when a type error occurs in MicroCaml."""
    pass

class DeclareError(Exception):
    """Raised when there's an error in variable declaration."""
    pass

class SelectError(Exception):
    """Raised when there's a record selection error."""
    pass

class DivByZeroError(Exception):
    """Raised when dividing by zero."""
    pass


# --------------------------
# 2. Tokens
# --------------------------

class Token:
    """Base class for all tokens in MicroCaml."""
    pass

class Tok_Int(Token):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Tok_Int({self.value})"

class Tok_Bool(Token):
    def __init__(self, value: bool):
        self.value = value

    def __repr__(self):
        return f"Tok_Bool({self.value})"

class Tok_String(Token):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"Tok_String({self.value})"

class Tok_ID(Token):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Tok_ID({self.name})"

class Tok_LParen(Token):
    def __repr__(self):
        return "Tok_LParen()"

class Tok_RParen(Token):
    def __repr__(self):
        return "Tok_RParen()"

class Tok_LCurly(Token):
    def __repr__(self):
        return "Tok_LCurly()"

class Tok_RCurly(Token):
    def __repr__(self):
        return "Tok_RCurly()"

class Tok_Dot(Token):
    def __repr__(self):
        return "Tok_Dot()"

class Tok_Equal(Token):
    def __repr__(self):
        return "Tok_Equal()"

class Tok_NotEqual(Token):
    def __repr__(self):
        return "Tok_NotEqual()"

class Tok_Greater(Token):
    def __repr__(self):
        return "Tok_Greater()"

class Tok_Less(Token):
    def __repr__(self):
        return "Tok_Less()"

class Tok_GreaterEqual(Token):
    def __repr__(self):
        return "Tok_GreaterEqual()"

class Tok_LessEqual(Token):
    def __repr__(self):
        return "Tok_LessEqual()"

class Tok_Or(Token):
    def __repr__(self):
        return "Tok_Or()"

class Tok_And(Token):
    def __repr__(self):
        return "Tok_And()"

class Tok_Not(Token):
    def __repr__(self):
        return "Tok_Not()"

class Tok_If(Token):
    def __repr__(self):
        return "Tok_If()"

class Tok_Then(Token):
    def __repr__(self):
        return "Tok_Then()"

class Tok_Else(Token):
    def __repr__(self):
        return "Tok_Else()"

class Tok_Add(Token):
    def __repr__(self):
        return "Tok_Add()"

class Tok_Sub(Token):
    def __repr__(self):
        return "Tok_Sub()"

class Tok_Mult(Token):
    def __repr__(self):
        return "Tok_Mult()"

class Tok_Div(Token):
    def __repr__(self):
        return "Tok_Div()"

class Tok_Concat(Token):
    def __repr__(self):
        return "Tok_Concat()"

class Tok_Let(Token):
    def __repr__(self):
        return "Tok_Let()"

class Tok_Def(Token):
    def __repr__(self):
        return "Tok_Def()"

class Tok_In(Token):
    def __repr__(self):
        return "Tok_In()"

class Tok_Rec(Token):
    def __repr__(self):
        return "Tok_Rec()"

class Tok_Fun(Token):
    def __repr__(self):
        return "Tok_Fun()"

class Tok_Arrow(Token):
    def __repr__(self):
        return "Tok_Arrow()"

class Tok_DoubleSemi(Token):
    def __repr__(self):
        return "Tok_DoubleSemi()"

class Tok_Semi(Token):
    def __repr__(self):
        return "Tok_Semi()"


# --------------------------
# 3. Operators
# --------------------------

class Op(Enum):
    ADD = auto()
    SUB = auto()
    MULT = auto()
    DIV = auto()
    CONCAT = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    OR = auto()
    AND = auto()


# --------------------------
# 4. Environment
# --------------------------
# For simplicity in Python, an environment can be a list of (var, Expr) pairs, 
# or a dictionary. We'll keep a list of tuples to stay close to the OCaml style.

Environment = List[Tuple[str, "Expr"]]


# --------------------------
# 5. Expressions (AST)
# --------------------------

class Expr:
    """Base class for all MicroCaml expressions."""
    pass

class IntExpr(Expr):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Int({self.value})"

    def __eq__(self, other):
        if not isinstance(other, IntExpr):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class BoolExpr(Expr):
    def __init__(self, value: bool):
        self.value = value

    def __repr__(self):
        return f"Bool({self.value})"

class StringExpr(Expr):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"

class ClosureExpr(Expr):
    def __init__(self, environment: Environment, var: str, body: "Expr"):
        self.environment = environment
        self.var = var
        self.body = body

    def __repr__(self):
        return f"Closure(env={self.environment}, var={self.var}, body={self.body})"

class IDExpr(Expr):
    def __init__(self, var: str):
        self.var = var

    def __repr__(self):
        return f"ID({self.var})"

    def __eq__(self, other):
        if not isinstance(other, IDExpr):
            return False
        return self.var == other.var

    def __hash__(self):
        return hash(self.var)


class FunExpr(Expr):
    def __init__(self, var: str, body: Expr):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"Fun({self.var}, {self.body})"

class NotExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def __repr__(self):
        return f"Not({self.expr})"

class BinopExpr(Expr):
    def __init__(self, op: Op, left: Expr, right: Expr):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Binop({self.op}, {self.left}, {self.right})"

    def __eq__(self, other):
        if not isinstance(other, BinopExpr):
            return False
        return self.op == other.op and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.op, self.left, self.right))

class IfExpr(Expr):
    def __init__(self, cond: Expr, then_expr: Expr, else_expr: Expr):
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

    def __repr__(self):
        return f"If({self.cond}, Then {self.then_expr} Else {self.else_expr})"

class AppExpr(Expr):
    def __init__(self, func: Expr, arg: Expr):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"App({self.func}, {self.arg})"

class LetExpr(Expr):
    def __init__(self, var: str, is_rec: bool, value_expr: Expr, body_expr: Expr):
        self.var = var
        self.is_rec = is_rec
        self.value_expr = value_expr
        self.body_expr = body_expr

    def __repr__(self):
        return f"Let({self.var}, rec={self.is_rec}, {self.value_expr}, {self.body_expr})"

class RecordExpr(Expr):
    def __init__(self, fields: List[Tuple[str, Expr]]):
        # fields: List of (label, expr) pairs
        self.fields = fields

    def __repr__(self):
        return f"Record({self.fields})"

class SelectExpr(Expr):
    def __init__(self, label: str, record: Expr):
        self.label = label
        self.record = record

    def __repr__(self):
        return f"Select({self.label}, {self.record})"

class Label(Expr):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"Lab({repr(self.var)})"

# --------------------------
# 6. Top-level directives (mutop)
# --------------------------

class Mutop:
    """Base class for top-level directives."""
    pass

class DefMutop(Mutop):
    def __init__(self, var: str, expr: Expr):
        self.var = var
        self.expr = expr

    def __repr__(self):
        return f"Def({self.var}, {self.expr})"

class ExprMutop(Mutop):
    def __init__(self, expr: Expr):
        self.expr = expr

    def __repr__(self):
        return f"Expr({self.expr})"

class NoOpMutop(Mutop):
    def __repr__(self):
        return "NoOp()"
