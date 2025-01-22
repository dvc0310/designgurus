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


def eval_expr_cps(env, e, k):
    if isinstance(e, IntExpr):
        return k(e.value)
    elif isinstance(e, StringExpr):
        return k(e.value)
    elif isinstance(e, BoolExpr):
        return k(e.value)
    elif isinstance(e, IDExpr):
        return k(lookup(env, e.var))
    elif isinstance(e, FunExpr):
        return eval_fun_cps(env, e, k)
    elif isinstance(e, AppExpr):
        return eval_app_cps(env, e, k)
    elif isinstance(e, NotExpr):
        return eval_expr_cps(env, e.expr, lambda v: k(not v))
    elif isinstance(e, BinopExpr):
        return eval_binop_cps(env, e, k)
    elif isinstance(e, IfExpr):
        def if_continuation(cond_val):
            if cond_val:
                return eval_expr_cps(env, e.then_expr, k)
            else:
                return eval_expr_cps(env, e.else_expr, k)
        return eval_expr_cps(env, e.cond, if_continuation)
    elif isinstance(e, LetExpr):
        return eval_let_expr_cps(env, e, k)
    else:
        raise NotImplementedError(f"Unimplemented expression type: {type(e)}")

def eval_let_expr_cps(env, e, k):
    if e.is_rec:
        def recursive_let_continuation(value):
            update(temp_env, e.var, value)
            return eval_expr_cps(temp_env, e.body_expr, k)

        temp_env = extend_tmp(env, e.var)
        return eval_expr_cps(temp_env, e.value_expr, recursive_let_continuation)
    else:
        def non_recursive_let_continuation(value):
            new_env = extend(env, e.var, value)
            return eval_expr_cps(new_env, e.body_expr, k)

        return eval_expr_cps(env, e.value_expr, non_recursive_let_continuation)

def eval_select_cps(env, e, k):
    def continue_with_record(record):
        if not isinstance(record, dict):
            raise TypeError("Not a record")
        if e.label in record:
            return k(record[e.label])
        else:
            raise SelectError(f"Label {e.label} not found")
    
    # Correcting e.expr to e.record to match the SelectExpr class definition
    return eval_expr_cps(env, e.record, continue_with_record)


def eval_binop_cps(env, e, k):
    def eval_right_continuation(left_val):
        def apply_op_continuation(right_val):
            return k(apply_op_with_type_check(e.op, left_val, right_val))
        return eval_expr_cps(env, e.right, apply_op_continuation)
    return eval_expr_cps(env, e.left, eval_right_continuation)

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

def eval_fun_cps(env, e, k):
    return k(ClosureExpr(env, e.var, e.body))

def eval_record_cps(env, e, k):
    evaluated_fields = []

    def eval_field(field_list):
        if not field_list:
            # All fields evaluated, continue with the evaluated record
            return k(dict(evaluated_fields))
        label, expr = field_list[0]
        def continue_with_value(value):
            evaluated_fields.append((label.var, value))
            return eval_field(field_list[1:])
        
        return eval_expr_cps(env, expr, continue_with_value)

    return eval_field(e.fields)


def eval_app_cps(env, e, k):
    def continue_with_closure(closure):
        def continue_with_arg(arg):
            if not isinstance(closure, ClosureExpr):
                raise TypeError("Attempting to call a non-function")
            
            closure_env, param, body_expr = closure.environment, closure.var, closure.body
            
            new_env = extend(closure_env, param, arg)
            
            return eval_expr_cps(new_env, body_expr, k)
        
        return eval_expr_cps(env, e.arg, continue_with_arg)
    
    return eval_expr_cps(env, e.func, continue_with_closure)

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

def eval_expr(env, e):
    return eval_expr_cps(env, e, lambda x: x)

def eval_mutop(env, mutop):
    if isinstance(mutop, DefMutop):
        def continuation(value):
            new_env = extend(env, mutop.var, value)
            return new_env, value
        return eval_expr_cps(env, mutop.expr, continuation)

    elif isinstance(mutop, ExprMutop):
        def continuation(value):
            return env, value
        return eval_expr_cps(env, mutop.expr, continuation)

    elif isinstance(mutop, NoOpMutop):
        return env, None

    else:
        raise NotImplementedError(f"Unhandled mutop directive type: {type(mutop)}")
