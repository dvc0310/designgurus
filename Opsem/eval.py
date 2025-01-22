from lexer import *
from microcaml import *
from parser__ import *

class DeclareError(Exception):
    pass

class DivByZeroError(Exception):
    pass

def extend(env, x, v):
    return [(x, v)] + env

def lookup(env, x):
    if not env:
        raise DeclareError(f"Unbound variable {x}")
    var, value = env[0]
    if x == var:
        return value
    return lookup(env[1:], x)

def extend_tmp(env, x):
    return [(x, 0)] + env

def update(env, x, v):
    if not env:
        raise DeclareError(f"Unbound variable {x}")
    var, _ = env[0]
    if x == var:
        env[0] = (var, v)
    else:
        update(env[1:], x, v)

def eval_expr(env, e):
    if isinstance(e, IntExpr):
        return e.value
    elif isinstance(e, StringExpr):
        return e.value
    elif isinstance(e, BoolExpr):
        return e.value
    elif isinstance(e, IDExpr):
        value = lookup(env, e.var)
        return value
    elif isinstance(e, FunExpr):
        closure = ClosureExpr(env, e.var, e.body)
        # Create a closure/define a function, capturing the current environment 'env', the parameter 'e.var' (e.g., 'n'), and the body 'e.body' (e.g., 'if n = 0 then 1 else ...')
        return closure
    elif isinstance(e, AppExpr):
        func = eval_expr(env, e.func)  # Look up the function "f" and get the function to call
        evaluated_value = eval_expr(env, e.arg)  # Look up 'n' and evaluate the argument expression (e.g., 'n - 1' in 'f(n - 1)'). e.arg is n - 1 here, and arg is the evaluated_value
        param, body_expr = func.var, func.body
        new_env = extend(func.environment, param, evaluated_value) # To the function environement, get the parameter 'n' and set its val to 'evaluated_value' (the evaluated n-1)
        # Create a new environment by extending the closure's environment with the parameter 'n' and the evaluated argument (e.g., '2' in the first call)
        return eval_expr(new_env, body_expr)  # Evaluate the body of the function (the 'if' expression) in this new environment
    elif isinstance(e, NotExpr):
        return not eval_expr(env, e.expr)
    elif isinstance(e, BinopExpr):
        left_val = eval_expr(env, e.left)
        right_val = eval_expr(env, e.right)
        result = apply_op_with_type_check(e.op, left_val, right_val)
        return result
    elif isinstance(e, IfExpr):
        cond_val = eval_expr(env, e.cond)  # Evaluate the condition of the 'if' expression (e.g., 'n = 0')
        if cond_val:
            return eval_expr(env, e.then_expr)  # If the condition is true, evaluate the 'then' branch (e.g., '1')
        else:
            return eval_expr(env, e.else_expr)  # If the condition is false, evaluate the 'else' branch (e.g., 'n * f (n - 1)')
    elif isinstance(e, LetExpr):
        if e.is_rec:
            temp_env = extend_tmp(env, e.var)
            # Create a temporary environment with a dummy value for 'f' (to handle recursive calls within the function definition)
            value = eval_expr(temp_env, e.value_expr)
            # Evaluate the function definition ('fun n -> ...') in this temporary environment
            update(temp_env, e.var, value)
            # Update 'f' in the temporary environment with the actual closure (so that recursive calls can find it)
            return eval_expr(temp_env, e.body_expr)
            # Evaluate the body of the 'let' expression (e.g., 'f 2') in the environment where 'f' is defined
        else:
            value = eval_expr(env, e.value_expr)
            new_env = extend(env, e.var, value)
            return eval_expr(new_env, e.body_expr)
    else:
        raise NotImplementedError(f"Unimplemented expression type: {type(e)}")

def eval_select(env, e):
    record = eval_expr(env, e.record)
    if not isinstance(record, dict):
        raise TypeError("Not a record")
    if e.label in record:
        return record[e.label]
    else:
        raise SelectError(f"Label {e.label} not found")

def apply_op_with_type_check(op, l, r):
    if op in {Op.ADD, Op.SUB, Op.MULT, Op.DIV, Op.GREATER, Op.LESS,
              Op.GREATER_EQUAL, Op.LESS_EQUAL}:
        if not isinstance(l, int) or not isinstance(r, int):
            raise TypeError(f"Operator {op} requires integer operands")
    elif op == Op.CONCAT:
        if not isinstance(l, str) or not isinstance(r, str):
            raise TypeError("Concat operation requires string operands")
    elif op in {Op.OR, Op.AND}:
        if not isinstance(l, bool) or not isinstance(r, bool):
            raise TypeError(f"Operator {op} requires boolean operands")
    elif op in {Op.EQUAL, Op.NOT_EQUAL}:
        pass
    else:
        raise NotImplementedError(f"Operator {op} not handled")
    return apply_op(op, l, r)

def eval_mutop(env, mutop):
    if isinstance(mutop, DefMutop):
        value = eval_expr(env, mutop.expr)
        new_env = extend(env, mutop.var, value)
        return new_env, value
    elif isinstance(mutop, ExprMutop):
        value = eval_expr(env, mutop.expr)
        return env, value
    elif isinstance(mutop, NoOpMutop):
        return env, None
    else:
        raise NotImplementedError(f"Unhandled mutop directive type: {type(mutop)}")

def apply_op(op, l, r):
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
    if op == Op.CONCAT:
        return l + r
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
    if op == Op.OR:
        return l or r
    if op == Op.AND:
        return l and r
    raise NotImplementedError(f"Operation {op} not handled")