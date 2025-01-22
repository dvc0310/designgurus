"""
Implements the same CFG as the OCaml code:

E -> id = num | { L }
L -> E ; L | ε

Builds an AST in Python, and simultaneously populates the parsetree graph 'g'.
No 'for' or 'while' loops are used; everything is done recursively.
"""

from lexer import (
    TOK_ID, TOK_NUM, TOK_SEMI, TOK_LCURLY, TOK_RCURLY,
    TOK_ASSIGN, TOK_END, tok_to_str
)

from parsetree import (
    g, add_node, Node
)

class ParseError(Exception):
    pass

# AST definitions in Python
class Exp:
    pass

class Assign(Exp):
    def __init__(self, var, val):
        self.var = var
        self.val = val

    def __repr__(self):
        return f"Assign({self.var}, {self.val})"

class Seq(Exp):
    def __init__(self, l):
        self.l = l

    def __repr__(self):
        return f"Seq({self.l})"

class L:
    pass

class LPair(L):
    def __init__(self, exp, l):
        self.exp = exp
        self.l = l

    def __repr__(self):
        return f"LPair({self.exp}, {self.l})"

class Skip(L):
    def __repr__(self):
        return "Skip()"

###########################################################
# We define the recursive-descent parser with no loops.   #
###########################################################

def lookahead(tokens, pos):
    if pos >= len(tokens):
        raise ParseError("no tokens left")
    return tokens[pos]

def match_tok(tokens, pos, kind_expected):
    if pos >= len(tokens):
        raise ParseError("no tokens to match")
    (kind, val) = tokens[pos]
    if kind == kind_expected:
        return pos+1
    else:
        raise ParseError(f"bad match: expected {kind_expected}, got {tok_to_str(tokens[pos])}")

def parse_E(parent, tokens, pos):
    print(f"parse_E at position {pos}, token: {tok_to_str(lookahead(tokens, pos))}")
    (kind, val) = lookahead(tokens, pos)

    if kind == TOK_ID:
        print(f"Parsing assignment for ID '{val}'")
        pos = match_tok(tokens, pos, TOK_ID)
        pos = match_tok(tokens, pos, TOK_ASSIGN)
        (k2, v2) = lookahead(tokens, pos)
        if k2 != TOK_NUM:
            raise ParseError("Expected NUM after '='")
        pos = match_tok(tokens, pos, TOK_NUM)
        print(f"Completed assignment: {val} = {v2}")
        return (pos, Assign(val, v2))

    elif kind == TOK_LCURLY:
        print("Parsing block (curly braces)")
        pos = match_tok(tokens, pos, TOK_LCURLY)
        (pos, lnode) = parse_L(parent, tokens, pos)
        pos = match_tok(tokens, pos, TOK_RCURLY)
        print("Completed block")
        return (pos, Seq(lnode))

    else:
        raise ParseError("Unexpected token")


def parse_L(parent, tokens, pos):
    """
    L -> E ; L | ε
    """
    (k, v) = lookahead(tokens, pos)
    print(f"parse_L at position {pos}, token: {tok_to_str((k, v))}")

    if k in [TOK_ID, TOK_LCURLY]:
        print("Branch: L -> E ; L")
        # Add E node to the parse tree
        nd_E = add_node(g, parent, "E")
        (pos, e_ast) = parse_E(nd_E, tokens, pos)

        # Match semicolon
        pos = match_tok(tokens, pos, TOK_SEMI)
        nd_semi = add_node(g, parent, ";")
        print(f"Matched semicolon at position {pos - 1}")

        # Add L node to the parse tree and recurse
        nd_L2 = add_node(g, parent, "L")
        print("Recursing into parse_L for next L")
        (pos, l_ast) = parse_L(nd_L2, tokens, pos)

        print(f"Returning from parse_L with LPair: ({e_ast}, {l_ast})")
        return (pos, LPair(e_ast, l_ast))
    else:
        print("Branch: L -> ε (empty production)")
        # Add ε node to the parse tree
        add_node(g, parent, "ε")
        print(f"Returning from parse_L with Skip() at position {pos}")
        return (pos, Skip())

def parse(tokens):
    """
    Top-level parse of a single E, then expect TOK_END. 
    We'll add a "root" node to parallel the original code's "parent".
    """
    root = add_node(g, None, "root")
    pos = 0
    (pos, ast) = parse_E(root, tokens, pos)

    (kind_end, val_end) = lookahead(tokens, pos)
    if kind_end != TOK_END:
        raise ParseError("Extra tokens after parse")
    return ast
