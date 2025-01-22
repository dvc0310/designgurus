# parser.py

from lexer import *
from microcaml import *

class ParseError(Exception):
    """Custom exception for parse errors."""
    def __init__(self, message):
        super().__init__(message)

def lookahead(tokens):
    """Return the next token without consuming it."""
    if not tokens:
        raise ParseError("No tokens available")
    return tokens[0]

def match_token(tokens, token_type):
    """
    Consumes the current token if it matches the expected class/type.
    Raises a ParseError otherwise.
    """
    if not tokens:
        raise ParseError("Unexpected end of input")

    curr = tokens[0]
    if isinstance(curr, token_type):
        return tokens[1:]
    else:
        raise ParseError(f"Expected {token_type.__name__}, got {curr}")

# --------------------------------------------------------------------
# 0. parse_mutop()
# --------------------------------------------------------------------

def parse_mutop(tokens):
    """
    Mutop parsing: 
      - ';;' => NoOp
      - 'def x = expr;;' => DefMutop(x, expr)
      - otherwise expr
    """
    if not tokens or isinstance(lookahead(tokens), Tok_DoubleSemi):
        return ([], NoOpMutop())
    elif isinstance(lookahead(tokens), Tok_Def):
        t1 = match_token(tokens, Tok_Def)
        var_name = lookahead(t1)
        t2 = match_token(t1, Tok_ID)
        t3 = match_token(t2, Tok_Equal)

        expr, remaining = parse_expr(t3)
        if remaining and isinstance(lookahead(remaining), Tok_DoubleSemi):
            return (match_token(remaining, Tok_DoubleSemi), DefMutop(var_name.name, expr))     
        
    # Otherwise it's an expression
    expr, remaining = parse_expr(tokens)
    return (match_token(remaining, Tok_DoubleSemi), ExprMutop(expr))

# --------------------------------------------------------------------
# 1. Top-Level parse()
# --------------------------------------------------------------------

def parse(tokens):
    """
    Entry point for the parser.
    Parses the entire token list into an AST (Expr).
    Ensures all tokens are consumed.
    """
    expr, remaining = parse_expr(tokens)
    if remaining:
        raise ParseError(f"Unexpected tokens after parsing: {remaining}")
    return expr

# --------------------------------------------------------------------
# 2. parse_expr
#
#    Expr -> LetExpr
#           | IfExpr
#           | FunctionExpr
#           | OrExpr
# --------------------------------------------------------------------

def parse_expr(tokens):
    """
    According to the grammar:
      Expr -> LetExpr | IfExpr | FunctionExpr | OrExpr
    """
    if not tokens:
        raise ParseError("No tokens to parse for expression")

    # Try parse_let_expr
    try:
        return parse_let_expr(tokens)
    except ParseError:
        pass

    # Try parse_if_expr
    try:
        return parse_if_expr(tokens)
    except ParseError:
        pass

    # Try parse_fun_expr
    try:
        return parse_fun_expr(tokens)
    except ParseError:
        pass

    # Fallback to OrExpr
    return parse_or_expr(tokens)

# --------------------------------------------------------------------
# 3. Specialized expressions: let, if, fun
# --------------------------------------------------------------------

def parse_let_expr(tokens):
    """
    LetExpr -> let Recursion Tok_ID = Expr in Expr
    Recursion -> rec | ε
    """
    if not tokens or not isinstance(lookahead(tokens), Tok_Let):
        raise ParseError("Not a let expression")

    tokens = match_token(tokens, Tok_Let)

    # Check for optional 'rec'
    is_rec = False
    if tokens and isinstance(lookahead(tokens), Tok_Rec):
        tokens = match_token(tokens, Tok_Rec)
        is_rec = True

    # Next must be an ID
    id_tok = lookahead(tokens)
    if not isinstance(id_tok, Tok_ID):
        raise ParseError("Expected ID after let/let rec")
    var_name = id_tok.name
    tokens = match_token(tokens, Tok_ID)

    # Must match '='
    tokens = match_token(tokens, Tok_Equal)

    # Parse the value expression
    value_expr, tokens = parse_expr(tokens)

    # Must match 'in'
    tokens = match_token(tokens, Tok_In)

    # Parse the body expression
    body_expr, tokens = parse_expr(tokens)

    return LetExpr(var_name, is_rec, value_expr, body_expr), tokens

def parse_if_expr(tokens):
    """
    IfExpr -> if Expr then Expr else Expr
    """
    if not tokens or not isinstance(lookahead(tokens), Tok_If):
        raise ParseError("Not an if expression")

    tokens = match_token(tokens, Tok_If)

    # Parse condition
    cond_expr, tokens = parse_expr(tokens)

    # then
    tokens = match_token(tokens, Tok_Then)

    # then-expression
    then_expr, tokens = parse_expr(tokens)

    # else
    tokens = match_token(tokens, Tok_Else)

    # else-expression
    else_expr, tokens = parse_expr(tokens)

    return IfExpr(cond_expr, then_expr, else_expr), tokens

def parse_fun_expr(tokens):
    """
    FunctionExpr -> fun Tok_ID -> Expr
    """
    if not tokens or not isinstance(lookahead(tokens), Tok_Fun):
        raise ParseError("Not a function expression")

    tokens = match_token(tokens, Tok_Fun)

    # Next must be an ID
    id_tok = lookahead(tokens)
    if not isinstance(id_tok, Tok_ID):
        raise ParseError("Expected ID after 'fun'")
    var_name = id_tok.name
    tokens = match_token(tokens, Tok_ID)

    # Must match '->'
    tokens = match_token(tokens, Tok_Arrow)

    # Parse the function body
    body_expr, tokens = parse_expr(tokens)

    return FunExpr(var_name, body_expr), tokens

# --------------------------------------------------------------------
# 4. OrExpr (includes left-associative chain with ||)
#
#    OrExpr -> AndExpr || OrExpr
#            | AndExpr
# --------------------------------------------------------------------

def parse_or_expr(tokens):
    left_expr, tokens = parse_and_expr(tokens)
    return parse_or_expr_tail(left_expr, tokens)

def parse_or_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_Or):
        tokens = match_token(tokens, Tok_Or)
        right_expr, tokens = parse_and_expr(tokens)
        new_expr = BinopExpr(Op.OR, left_expr, right_expr)
        return parse_or_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 5. AndExpr (includes left-associative chain with &&)
#
#    AndExpr -> EqualityExpr && AndExpr
#             | EqualityExpr
# --------------------------------------------------------------------

def parse_and_expr(tokens):
    left_expr, tokens = parse_equality_expr(tokens)
    return parse_and_expr_tail(left_expr, tokens)

def parse_and_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_And):
        tokens = match_token(tokens, Tok_And)
        right_expr, tokens = parse_equality_expr(tokens)
        new_expr = BinopExpr(Op.AND, left_expr, right_expr)
        return parse_and_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 6. EqualityExpr
#
#    EqualityExpr -> RelationalExpr EqualityOperator EqualityExpr
#                  | RelationalExpr
#
#    EqualityOperator -> = | <>
# --------------------------------------------------------------------

def parse_equality_expr(tokens):
    left_expr, tokens = parse_relational_expr(tokens)
    return parse_equality_expr_tail(left_expr, tokens)

def parse_equality_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_Equal):
        tokens = match_token(tokens, Tok_Equal)
        right_expr, tokens = parse_relational_expr(tokens)
        new_expr = BinopExpr(Op.EQUAL, left_expr, right_expr)
        return parse_equality_expr_tail(new_expr, tokens)
    elif isinstance(la, Tok_NotEqual):
        tokens = match_token(tokens, Tok_NotEqual)
        right_expr, tokens = parse_relational_expr(tokens)
        new_expr = BinopExpr(Op.NOT_EQUAL, left_expr, right_expr)
        return parse_equality_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 7. RelationalExpr
#
#    RelationalExpr -> AdditiveExpr RelationalOperator RelationalExpr
#                    | AdditiveExpr
#
#    RelationalOperator -> < | > | <= | >=
# --------------------------------------------------------------------

def parse_relational_expr(tokens):
    left_expr, tokens = parse_additive_expr(tokens)
    return parse_relational_expr_tail(left_expr, tokens)

def parse_relational_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_Less):
        tokens = match_token(tokens, Tok_Less)
        right_expr, tokens = parse_additive_expr(tokens)
        new_expr = BinopExpr(Op.LESS, left_expr, right_expr)
        return parse_relational_expr_tail(new_expr, tokens)
    elif isinstance(la, Tok_Greater):
        tokens = match_token(tokens, Tok_Greater)
        right_expr, tokens = parse_additive_expr(tokens)
        new_expr = BinopExpr(Op.GREATER, left_expr, right_expr)
        return parse_relational_expr_tail(new_expr, tokens)
    elif isinstance(la, Tok_LessEqual):
        tokens = match_token(tokens, Tok_LessEqual)
        right_expr, tokens = parse_additive_expr(tokens)
        new_expr = BinopExpr(Op.LESS_EQUAL, left_expr, right_expr)
        return parse_relational_expr_tail(new_expr, tokens)
    elif isinstance(la, Tok_GreaterEqual):
        tokens = match_token(tokens, Tok_GreaterEqual)
        right_expr, tokens = parse_additive_expr(tokens)
        new_expr = BinopExpr(Op.GREATER_EQUAL, left_expr, right_expr)
        return parse_relational_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 8. AdditiveExpr
#
#    AdditiveExpr -> MultiplicativeExpr AdditiveOperator AdditiveExpr
#                   | MultiplicativeExpr
#
#    AdditiveOperator -> + | -
# --------------------------------------------------------------------

def parse_additive_expr(tokens):
    left_expr, tokens = parse_multiplicative_expr(tokens)
    return parse_additive_expr_tail(left_expr, tokens)

def parse_additive_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_Add):
        tokens = match_token(tokens, Tok_Add)
        right_expr, tokens = parse_multiplicative_expr(tokens)
        new_expr = BinopExpr(Op.ADD, left_expr, right_expr)
        return parse_additive_expr_tail(new_expr, tokens)
    elif isinstance(la, Tok_Sub):
        tokens = match_token(tokens, Tok_Sub)
        right_expr, tokens = parse_multiplicative_expr(tokens)
        new_expr = BinopExpr(Op.SUB, left_expr, right_expr)
        return parse_additive_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 9. MultiplicativeExpr
#
#    MultiplicativeExpr -> ConcatExpr MultiplicativeOperator MultiplicativeExpr
#                         | ConcatExpr
#
#    MultiplicativeOperator -> * | /
# --------------------------------------------------------------------

def parse_multiplicative_expr(tokens):
    left_expr, tokens = parse_concat_expr(tokens)
    return parse_multiplicative_expr_tail(left_expr, tokens)

def parse_multiplicative_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_Mult):
        tokens = match_token(tokens, Tok_Mult)
        right_expr, tokens = parse_concat_expr(tokens)
        new_expr = BinopExpr(Op.MULT, left_expr, right_expr)
        return parse_multiplicative_expr_tail(new_expr, tokens)
    elif isinstance(la, Tok_Div):
        tokens = match_token(tokens, Tok_Div)
        right_expr, tokens = parse_concat_expr(tokens)
        new_expr = BinopExpr(Op.DIV, left_expr, right_expr)
        return parse_multiplicative_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 10. ConcatExpr
#
#    ConcatExpr -> UnaryExpr ^ ConcatExpr
#                 | UnaryExpr
# --------------------------------------------------------------------

def parse_concat_expr(tokens):
    left_expr, tokens = parse_unary_expr(tokens)
    return parse_concat_expr_tail(left_expr, tokens)

def parse_concat_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_Concat):  # '^' operator
        tokens = match_token(tokens, Tok_Concat)
        right_expr, tokens = parse_concat_expr(tokens)
        new_expr = BinopExpr(Op.CONCAT, left_expr, right_expr)
        return parse_concat_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 11. UnaryExpr
#
#    UnaryExpr -> not UnaryExpr
#                | AppExpr
# --------------------------------------------------------------------

def parse_unary_expr(tokens):
    if not tokens:
        raise ParseError("No tokens in parse_unary_expr")

    la = lookahead(tokens)
    if isinstance(la, Tok_Not):
        # 'not' operator
        tokens = match_token(tokens, Tok_Not)
        subexpr, tokens = parse_unary_expr(tokens)
        return NotExpr(subexpr), tokens
    else:
        return parse_app_expr(tokens)

# --------------------------------------------------------------------
# 12. AppExpr
#
#    AppExpr -> left-associative function application
#      (Gram. simplified as: AppExpr -> SelectExpr PrimaryExpr | SelectExpr)
#
#    We'll implement a typical left-associative parse:
#      parse_app_expr -> parse_select_expr -> parse_app_expr_tail
# --------------------------------------------------------------------

def parse_app_expr(tokens):
    """
    AppExpr -> PrimaryExpr AppExprTail
    """
    base_expr, tokens = parse_select_expr(tokens)
    return parse_app_expr_tail(base_expr, tokens)

def parse_app_expr_tail(func_expr, tokens):
    """
    AppExprTail -> PrimaryExpr AppExprTail
                 | ε
    Left-associative:
      e1 e2 e3 => App(App(e1, e2), e3)
    """
    if not tokens:
        return func_expr, tokens

    # Try to parse another PrimaryExpr to treat as an argument
    try:
        arg_expr, tokens2 = parse_primary_expr(tokens)
        new_expr = AppExpr(func_expr, arg_expr)
        # Tail recurse to see if more arguments follow
        return new_expr, tokens2
    except ParseError:
        # If we can't parse a valid primary, then there's no more application
        return func_expr, tokens
# --------------------------------------------------------------------
# 13. SelectExpr
#
#    SelectExpr -> PrimaryExpr . Tok_ID
#                | PrimaryExpr
# --------------------------------------------------------------------

def parse_select_expr(tokens):
    base_expr, tokens = parse_primary_expr(tokens)
    return parse_select_expr_tail(base_expr, tokens)

def parse_select_expr_tail(left_expr, tokens):
    if not tokens:
        return left_expr, tokens

    la = lookahead(tokens)
    if isinstance(la, Tok_Dot):
        tokens = match_token(tokens, Tok_Dot)
        # Next must be ID
        id_tok = lookahead(tokens)
        if not isinstance(id_tok, Tok_ID):
            raise ParseError("Expected ID after '.'")
        tokens = match_token(tokens, Tok_ID)

        new_expr = SelectExpr(label=id_tok.name, record=left_expr)
        return parse_select_expr_tail(new_expr, tokens)
    else:
        return left_expr, tokens

# --------------------------------------------------------------------
# 14. PrimaryExpr
#
#    PrimaryExpr -> Tok_Int
#                  | Tok_Bool
#                  | Tok_String
#                  | Tok_ID
#                  | ( Expr )
#                  | RecordExpr
# --------------------------------------------------------------------

def parse_primary_expr(tokens):
    if not tokens:
        raise ParseError("No tokens in parse_primary_expr")

    la = lookahead(tokens)

    # Int literal
    if isinstance(la, Tok_Int):
        tokens = match_token(tokens, Tok_Int)
        return IntExpr(la.value), tokens

    # Bool literal
    if isinstance(la, Tok_Bool):
        tokens = match_token(tokens, Tok_Bool)
        return BoolExpr(la.value), tokens

    # String literal
    if isinstance(la, Tok_String):
        tokens = match_token(tokens, Tok_String)
        return StringExpr(la.value), tokens

    # Identifier
    if isinstance(la, Tok_ID):
        tokens = match_token(tokens, Tok_ID)
        return IDExpr(la.name), tokens

    # Parenthesized expression
    if isinstance(la, Tok_LParen):
        tokens = match_token(tokens, Tok_LParen)
        expr, tokens = parse_expr(tokens)
        tokens = match_token(tokens, Tok_RParen)
        return expr, tokens

    # Record expression: '{' ... '}'
    if isinstance(la, Tok_LCurly):
        # Could be an empty record or a record with fields
        tokens = match_token(tokens, Tok_LCurly)
        la2 = lookahead(tokens)
        if isinstance(la2, Tok_RCurly):
            # Empty record
            tokens = match_token(tokens, Tok_RCurly)
            return RecordExpr([]), tokens
        else:
            # Record with fields
            fields, tokens = parse_record_body_expr(tokens)
            tokens = match_token(tokens, Tok_RCurly)
            return RecordExpr(fields), tokens

    raise ParseError(f"Unexpected token {la} in parse_primary_expr")

# --------------------------------------------------------------------
# 10. Record Body
# --------------------------------------------------------------------

def parse_record_body_expr(tokens):
    """
    RecordBody -> ( ID '=' Expr ( ';' RecordBody )? )?
    """
    # Possibly empty
    if not tokens:
        return [], tokens

    la = lookahead(tokens)
    if not isinstance(la, Tok_ID):
        # empty record
        return [], tokens

    # Parse one field
    var_name = la.name
    tokens = match_token(tokens, Tok_ID)
    tokens = match_token(tokens, Tok_Equal)
    value_expr, tokens = parse_expr(tokens)

    fields = [(var_name, value_expr)]

    # Check for ';' => more fields
    if tokens:
        la2 = lookahead(tokens)
        if isinstance(la2, Tok_Semi):
            tokens = match_token(tokens, Tok_Semi)
            more_fields, tokens = parse_record_body_expr(tokens)
            fields.extend(more_fields)

    return fields, tokens
