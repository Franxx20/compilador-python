import unittest
from parser import ejecutar_parser
from pathlib import Path

class TestParser(unittest.TestCase):
    def setUp(self):
        # Backup the original test file if it exists
        self.test_file = Path("./resources/parser_test_2.txt")
        self.original_content = None
        if self.test_file.exists():
            self.original_content = self.test_file.read_text()

    def tearDown(self):
        # Restore the original test file
        if self.original_content is not None:
            self.test_file.write_text(self.original_content)
        else:
            if self.test_file.exists():
                self.test_file.unlink()

    def run_parser_with_code(self, code):
        self.test_file.parent.mkdir(parents=True, exist_ok=True)
        self.test_file.write_text(code)
        try:
            ejecutar_parser()
        except Exception as e:
            return str(e)
        return "OK"

    def test_valid_declaration(self):
        code = "init { x, y : Int }"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_valid_assignment(self):
        code = "init { x : Int }\nx := 5"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_valid_while(self):
        code = "while (1 < 2) { init { x : Int } }"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_invalid_syntax(self):
        code = "init { x, : Int }"  # Invalid: comma before colon
        result = self.run_parser_with_code(code)
        self.assertIn("Error en la linea", result)

    # Additional tests below

    def test_multiple_declarations(self):
        code = "init { a, b : Int c, d : Float }"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_assignment_with_expression(self):
        code = "init { x : Int }\nx := 1 + 2 * 3"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_nested_while(self):
        code = "while (1 < 2) { while (2 < 3) { init { x : Int } } }"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_if_else(self):
        code = "if (x > 0) { x := x - 1 } else { x := 0 }"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_read_write(self):
        code = "init { x : Int }\nread(x)\nwrite(x)"
        result = self.run_parser_with_code(code)
        self.assertEqual(result, "OK")

    def test_invalid_missing_brace(self):
        code = "init { x : Int "
        result = self.run_parser_with_code(code)
        self.assertIn("Error en la linea", result)

    def test_invalid_assignment(self):
        code = "init { x : Int }\nx = 5"  # Should be ':='
        result = self.run_parser_with_code(code)
        self.assertIn("Error en la linea", result)

if __name__ == '__main__':
    unittest.main()