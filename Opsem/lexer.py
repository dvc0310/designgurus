# lexer.py

import re
from microcaml import *

# We add these here to match the original OCaml code.
# You can move them to microcaml.py if you prefer.
class Tok_END(Token):
    def __repr__(self):
        return "Tok_END()"

class IllegalExpression(Exception):
    """Raised when an illegal token is found during lexing."""
    pass
# Integers: also handle optional parentheses around negative numbers:
# e.g.,  "(-123)" or "123"

re_num = re.compile(r"\(-[0-9]+\)|[0-9]+")

# Strings: anything inside double quotes, no internal escaping logic here
re_string = re.compile(r'"(\\.|[^"\\])*"')

re_and = re.compile(r"&&")
re_or  = re.compile(r"\|\|")

# Whitespace
re_space = re.compile(r"[ \t\n\r]+")

# Multi-character operators
re_arrow = re.compile(r"->")
re_greater_equal = re.compile(r">=")
re_less_equal = re.compile(r"<=")
re_not_equal = re.compile(r"<>")
re_double_semi = re.compile(r";;")

# Single-character operators/punctuation
re_equal = re.compile(r"=")
re_greater = re.compile(r">")
re_less = re.compile(r"<")
re_add = re.compile(r"\+")
re_sub = re.compile(r"-")
re_mult = re.compile(r"\*")
re_div = re.compile(r"/")
re_concat = re.compile(r"\^")
re_semi = re.compile(r";")
re_dot = re.compile(r"\.")

# Parentheses and curly braces
re_lparen = re.compile(r"\(")
re_rparen = re.compile(r"\)")
re_lcurly = re.compile(r"\{")
re_rcurly = re.compile(r"\}")

# Keywords or identifiers: letters followed by letters/digits/underscores
re_keyword_or_id = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

########################################
# 4. Main tokenize function
########################################

def tokenize(s: str):
    """
    Converts a string into a list of tokens (Tok_*).
    Returns [Tok_END()] at the end.
    """

    def tok(pos, s):
        # End of input
        if pos >= len(s):
            return []
        
        # 1. Skip whitespace
        m = re_space.match(s, pos)
        if m:
            return tok(pos + len(m.group(0)), s)
        
       # Integer literal (possibly negative, possibly in parentheses)
        m = re_num.match(s, pos)
        if m:
            token_str = m.group(0)
            # If it's wrapped in parentheses, remove them:
            if token_str.startswith("(") and token_str.endswith(")"):
                token_str = token_str[1:-1]  # remove outer parentheses
            return [Tok_Int(int(token_str))] + tok(pos + len(m.group(0)), s)


        # String literal in double quotes
        m = re_string.match(s, pos)
        if m:
            full_str = m.group(0)         # e.g.,  "hello"
            inner_text = full_str[1:-1]   # Strip the quotes (e.g., hello)
            # Decode escaped characters
            inner_text = bytes(inner_text, "utf-8").decode("unicode_escape")
            return [Tok_String(inner_text)] + tok(pos + len(full_str), s)

                # 5. Keywords or identifiers
        m = re_keyword_or_id.match(s, pos)
        if m:
            token_str = m.group(0)

            # Check for recognized keywords:
            if token_str == "let":
                return [Tok_Let()] + tok(pos + 3, s)
            if token_str == "def":
                return [Tok_Def()] + tok(pos + 3, s)
            if token_str == "rec":
                return [Tok_Rec()] + tok(pos + 3, s)
            if token_str == "fun":
                return [Tok_Fun()] + tok(pos + 3, s)
            if token_str == "not":
                return [Tok_Not()] + tok(pos + 3, s)
            if token_str == "in":
                return [Tok_In()] + tok(pos + 2, s)
            if token_str == "if":
                return [Tok_If()] + tok(pos + 2, s)
            if token_str == "then":
                return [Tok_Then()] + tok(pos + 4, s)
            if token_str == "else":
                return [Tok_Else()] + tok(pos + 4, s)
            if token_str == "true":
                return [Tok_Bool(True)] + tok(pos + 4, s)
            if token_str == "false":
                return [Tok_Bool(False)] + tok(pos + 5, s)

            # Otherwise, it's an identifier
            return [Tok_ID(token_str)] + tok(pos + len(token_str), s)
        # 2. Multi-character operators first

        # '->'
        m = re_arrow.match(s, pos)
        if m:
            return [Tok_Arrow()] + tok(pos + 2, s)

        # '>='
        m = re_greater_equal.match(s, pos)
        if m:
            return [Tok_GreaterEqual()] + tok(pos + 2, s)

        # '<='
        m = re_less_equal.match(s, pos)
        if m:
            return [Tok_LessEqual()] + tok(pos + 2, s)
        
        # Match '&&'
        m = re_and.match(s, pos)
        if m:
            return [Tok_And()] + tok(pos + 2, s)

        # Match '||'
        m = re_or.match(s, pos)
        if m:
            return [Tok_Or()] + tok(pos + 2, s)

        # '<>'
        m = re_not_equal.match(s, pos)
        if m:
            return [Tok_NotEqual()] + tok(pos + 2, s)

        # ';;'
        m = re_double_semi.match(s, pos)
        if m:
            return [Tok_DoubleSemi()] + tok(pos + 2, s)

        # 3. Single-character tokens

        # '='
        m = re_equal.match(s, pos)
        if m:
            return [Tok_Equal()] + tok(pos + 1, s)

        # '>'
        m = re_greater.match(s, pos)
        if m:
            return [Tok_Greater()] + tok(pos + 1, s)

        # '<'
        m = re_less.match(s, pos)
        if m:
            return [Tok_Less()] + tok(pos + 1, s)

        # '+'
        m = re_add.match(s, pos)
        if m:
            return [Tok_Add()] + tok(pos + 1, s)

        # '-'
        m = re_sub.match(s, pos)
        if m:
            return [Tok_Sub()] + tok(pos + 1, s)

        # '*'
        m = re_mult.match(s, pos)
        if m:
            return [Tok_Mult()] + tok(pos + 1, s)

        # '/'
        m = re_div.match(s, pos)
        if m:
            return [Tok_Div()] + tok(pos + 1, s)

        # '^'
        m = re_concat.match(s, pos)
        if m:
            return [Tok_Concat()] + tok(pos + 1, s)

        # '.'
        m = re_dot.match(s, pos)
        if m:
            return [Tok_Dot()] + tok(pos + 1, s)

        # ';'
        m = re_semi.match(s, pos)
        if m:
            return [Tok_Semi()] + tok(pos + 1, s)

        # '('
        m = re_lparen.match(s, pos)
        if m:
            return [Tok_LParen()] + tok(pos + 1, s)

        # ')'
        m = re_rparen.match(s, pos)
        if m:
            return [Tok_RParen()] + tok(pos + 1, s)

        # '{'
        m = re_lcurly.match(s, pos)
        if m:
            return [Tok_LCurly()] + tok(pos + 1, s)

        # '}'
        m = re_rcurly.match(s, pos)
        if m:
            return [Tok_RCurly()] + tok(pos + 1, s)



        # If none of the above matches, we have an illegal token
        raise IllegalExpression(f"Unexpected token at position {pos}: {s[pos:pos+10]!r}")

    return tok(0, s)