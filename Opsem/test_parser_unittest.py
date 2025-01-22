# test_parser_unittest.py
import unittest
from parser__ import *
from microcaml import *

class TestParser(unittest.TestCase):
    def test_simple_let_binding(self):
        tokens = [
            Tok_Let(),
            Tok_ID("x"),
            Tok_Equal(),
            Tok_Int(5),
            Tok_In(),
            Tok_ID("x"),
            Tok_Add(),
            Tok_Int(3)
        ]
        ast = parse(tokens)
        expected_ast = LetExpr(
            var="x",
            is_rec=False,
            value_expr=IntExpr(5),
            body_expr=BinopExpr(op=Op.ADD, left=IDExpr("x"), right=IntExpr(3))
        )
        self.assertEqual(repr(ast), repr(expected_ast))

    def test_let_recursion_factorial(self):
        tokens = [
            Tok_Let(),
            Tok_Rec(),
            Tok_ID("factorial"),
            Tok_Equal(),
            Tok_Fun(),
            Tok_ID("n"),
            Tok_Arrow(),
            Tok_If(),
            Tok_ID("n"),
            Tok_Equal(),
            Tok_Int(0),
            Tok_Then(),
            Tok_Int(1),
            Tok_Else(),
            Tok_ID("n"),
            Tok_Mult(),
            Tok_ID("factorial"),
            Tok_LParen(),
            Tok_ID("n"),
            Tok_Sub(),
            Tok_Int(1),
            Tok_RParen(),
            Tok_In(),
            Tok_ID("factorial"),
            Tok_Int(5)
        ]
        ast = parse(tokens)
        # Due to complexity, check top-level LetExpr and its attributes
        self.assertIsInstance(ast, LetExpr)
        self.assertEqual(ast.var, "factorial")
        self.assertTrue(ast.is_rec)
        self.assertIsInstance(ast.value_expr, FunExpr)
        self.assertEqual(ast.value_expr.var, "n")
        self.assertIsInstance(ast.value_expr.body, IfExpr)
        self.assertIsInstance(ast.body_expr, AppExpr)
        self.assertEqual(ast.body_expr.func, IDExpr("factorial"))
        self.assertEqual(ast.body_expr.arg, IntExpr(5))

    def test_unexpected_token(self):
        tokens = [
            Tok_Let(),
            Tok_ID("x"),
            Tok_Equal(),
            Tok_In(),
            Tok_ID("x"),
            Tok_Add(),
            Tok_Int(1)
        ]
        with self.assertRaises(ParseError):
            parse(tokens)

    def test_if_expression_with_logical_and(self):
        tokens = [
            Tok_If(),
            Tok_Bool(True),
            Tok_And(),
            Tok_Bool(False),
            Tok_Then(),
            Tok_Int(1),
            Tok_Else(),
            Tok_Int(0)
        ]
        ast = parse(tokens)
        expected_ast = IfExpr(
            cond=BinopExpr(op=Op.AND, left=BoolExpr(True), right=BoolExpr(False)),
            then_expr=IntExpr(1),
            else_expr=IntExpr(0)
        )
        self.assertEqual(repr(ast), repr(expected_ast))

    def test_function_application(self):
        tokens = [
            Tok_LParen(),
            Tok_Fun(),
            Tok_ID("x"),
            Tok_Arrow(),
            Tok_ID("x"),
            Tok_Add(),
            Tok_Int(1),
            Tok_RParen(),
            Tok_Int(5)
        ]
        ast = parse(tokens)
        expected_ast = AppExpr(
            func=FunExpr(var="x", body=BinopExpr(op=Op.ADD, left=IDExpr("x"), right=IntExpr(1))),
            arg=IntExpr(5)
        )
        self.assertEqual(repr(ast), repr(expected_ast))

    # Add more tests as needed...

if __name__ == '__main__':
    unittest.main()
