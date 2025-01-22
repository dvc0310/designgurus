from lexer import *
from microcaml import *
from parser__ import *

class DeclareError(Exception):
    pass

class DivByZeroError(Exception):
    pass

def extend(env, x, v):
    """
    Adds mapping [x:v] to environment [env]
    """
    return [(x, v)] + env

def lookup(env, x):
    """
    Returns [v] if [x:v] is a mapping in [env]; uses the
    most recent if multiple mappings for [x] are present
    """
    if not env:
        raise DeclareError(f"Unbound variable {x}")
    var, value = env[0]
    if x == var:
        return value
    return lookup(env[1:], x)

def extend_tmp(env, x):
    """
    Creates a placeholder mapping for [x] in [env]; needed
    for handling recursive definitions
    """
    return [(x, 0)] + env

def update(env, x, v):
    """
    Updates the (most recent) mapping in [env] for [x] to [v]
    """
    if not env:
        raise DeclareError(f"Unbound variable {x}")
    var, _ = env[0]
    if x == var:
        env[0] = (var, v)
    else:
        update(env[1:], x, v)

# Evaluator functions
def eval_expr(env, e):
    """
    Evaluates expression [e] in environment [env].
    """
    def aux(env, stack, acc):
        e = stack.pop()
        if isinstance(e, IntExpr):
            return e.value
        elif isinstance(e, StringExpr):
            return e.value
        elif isinstance(e, BoolExpr):
            return e.value
        elif isinstance(e, IDExpr):
            return lookup(env, e.var)
        elif isinstance(e, NotExpr):
            return not eval_expr(env, e.expr)
        elif isinstance(e, BinopExpr):
            return eval_binop(env, e)
        elif isinstance(e, IfExpr):
            cond = eval_expr(env, e.cond)
            if not isinstance(cond, bool):
                raise TypeError("Condition in IfExpr must be a boolean")
            if cond:
                return eval_expr(env, e.then_expr)
            else:
                return eval_expr(env, e.else_expr)
        elif isinstance(e, LetExpr):
            return eval_let_expr(env, e)
        else:
            raise NotImplementedError(f"Unimplemented expression type: {type(e)}")

def eval_let_expr(env, e):
    """
    Evaluates a let expression [e] in environment [env].
    """
    if e.is_rec:
        # Create a temporary environment with a placeholder
        temp_env = extend_tmp(env, e.var)
        # Evaluate the value expression in the temporary environment
        value = eval_expr(temp_env, e.value_expr)
        # Update the environment with the actual value
        update(temp_env, e.var, value)
        # Evaluate the body expression with the updated environment
        return eval_expr(temp_env, e.body_expr)
    else:
        # Non-recursive let
        value = eval_expr(env, e.value_expr)
        new_env = extend(env, e.var, value)
        return eval_expr(new_env, e.body_expr)

def eval_binop(env, e):
    """
    Evaluates a binary operation expression `e` in the environment `env`.
    """
    left_val = eval_expr(env, e.left)
    right_val = eval_expr(env, e.right)
    
    # Perform type checking based on the operator
    if e.op in {Op.ADD, Op.SUB, Op.MULT, Op.DIV, Op.GREATER, Op.LESS,
                Op.GREATER_EQUAL, Op.LESS_EQUAL}:
        if not isinstance(left_val, int) or not isinstance(right_val, int):
            raise TypeError(f"Operator {e.op} requires integer operands")
    elif e.op == Op.CONCAT:
        if not isinstance(left_val, str) or not isinstance(right_val, str):
            raise TypeError("Concat operation requires string operands")
    elif e.op in {Op.OR, Op.AND}:
        if not isinstance(left_val, bool) or not isinstance(right_val, bool):
            raise TypeError(f"Operator {e.op} requires boolean operands")
    elif e.op in {Op.EQUAL, Op.NOT_EQUAL}:
        # Equality can be between any comparable types
        pass
    else:
        raise NotImplementedError(f"Operator {e.op} not handled")

    # Apply the operator
    result = apply_op(e.op, left_val, right_val)
    return result

def apply_op(op, l, r):
    # Arithmetic operations
    if op == Op.ADD:  
        return l + r
    if op == Op.SUB:  
        return l - r
    if op == Op.MULT: 
        return l * r
    if op == Op.DIV:
        if r == 0:
            raise DivByZeroError("Division by zero")
        return l // r

    # String concatenation
    if op == Op.CONCAT:
        return l + r

    # Relational operations
    if op == Op.GREATER:
        return l > r
    if op == Op.LESS:
        return l < r
    if op == Op.GREATER_EQUAL:
        return l >= r
    if op == Op.LESS_EQUAL:
        return l <= r
    if op == Op.EQUAL:
        return l == r
    if op == Op.NOT_EQUAL:
        return l != r

    # Logical operations
    if op == Op.OR:
        return l or r
    if op == Op.AND:
        return l and r

    raise NotImplementedError(f"Operation {op} not handled")