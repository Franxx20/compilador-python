import unittest
from lexer import lexer

def tokenize(code):
    lexer.input(code)
    return [(tok.type, tok.value) for tok in lexer]

class TestLexer(unittest.TestCase):
    def test_integer_token(self):
        tokens = tokenize("123")
        self.assertEqual(tokens, [("N_ENTERO", 123)])

    def test_float_token(self):
        tokens = tokenize("3.14")
        self.assertEqual(tokens, [("N_FLOAT", 3.14)])

    def test_identifier_token(self):
        tokens = tokenize("variable")
        self.assertEqual(tokens, [("ID", "variable")])

    def test_assignment_token(self):
        tokens = tokenize(":=")
        self.assertEqual(tokens, [("OP_ASIGNACION", ":=")])

    def test_keywords(self):
        tokens = tokenize("while init")
        self.assertEqual(tokens, [("WHILE", "while"), ("INIT", "init")])

    def test_operators(self):
        tokens = tokenize("+ - * /")
        self.assertEqual([t[0] for t in tokens], ["MAS", "MENOS", "MULTIPLICACION", "DIVISION"])

    def test_parentheses_and_braces(self):
        tokens = tokenize("( ) { }")
        self.assertEqual([t[0] for t in tokens], ["A_PARENTESIS", "C_PARENTESIS", "A_LLAVES", "C_LLAVES"])

    def test_comparison_operators(self):
        tokens = tokenize("== != >= <= > <")
        self.assertEqual([t[0] for t in tokens], [
            "IGUAL", "DISTINTO", "MAYOR_IGUAL", "MENOR_IGUAL", "MAYOR", "MENOR"
        ])

if __name__ == '__main__':
    unittest.main()