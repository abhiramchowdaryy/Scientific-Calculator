import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Scientific Calculator")
        self.setGeometry(100, 100, 450, 500)
        self.expression = ""
        self.memory = 0
        self.initUI()

    def initUI(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 20px; height: 40px;")

        mainLayout = QVBoxLayout()
        buttonLayout = QGridLayout()

        buttons = [
            '7', '8', '9', '/', 'sqrt',
            '4', '5', '6', '*', 'log',
            '1', '2', '3', '-', 'sin',
            '0', '.', '=', '+', 'cos',
            '(', ')', '^', 'C', 'tan',
            'ln', 'e^x', 'x!', '1/x', 'abs',
            'pi', 'e', 'mod', 'MC', 'MR',
            'M+', 'M-', '', '', ''
        ]

        positions = [(i, j) for i in range(7) for j in range(5)]

        for pos, btn_text in zip(positions, buttons):
            if not btn_text:
                continue
            button = QPushButton(btn_text)
            button.setStyleSheet("font-size: 16px; padding: 8px;")
            button.clicked.connect(self.on_button_clicked)
            buttonLayout.addWidget(button, *pos)

        mainLayout.addWidget(self.display)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def on_button_clicked(self):
        button = self.sender()
        text = button.text()

        if text == "C":
            self.expression = ""
            self.display.setText("")
        elif text == "=":
            try:
                result = self.evaluate(self.expression)
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""
        elif text == "MC":
            self.memory = 0
        elif text == "MR":
            self.expression += str(self.memory)
            self.display.setText(self.expression)
        elif text == "M+":
            try:
                self.memory += float(self.evaluate(self.expression))
                self.expression = ""
                self.display.setText("")
            except:
                self.display.setText("Error")
        elif text == "M-":
            try:
                self.memory -= float(self.evaluate(self.expression))
                self.expression = ""
                self.display.setText("")
            except:
                self.display.setText("Error")
        elif text in ["pi", "e"]:
            const = str(math.pi) if text == "pi" else str(math.e)
            self.expression += const
            self.display.setText(self.expression)
        else:
            self.expression += text
            self.display.setText(self.expression)

    def evaluate(self, expr):
        expr = expr.replace('^', '**')

        func_map = {
            'sqrt': lambda x: math.sqrt(float(x)),
            'log': lambda x: math.log10(float(x)),
            'ln': lambda x: math.log(float(x)),
            'sin': lambda x: math.sin(math.radians(float(x))),
            'cos': lambda x: math.cos(math.radians(float(x))),
            'tan': lambda x: math.tan(math.radians(float(x))),
            'e^x': lambda x: math.exp(float(x)),
            'x!': lambda x: math.factorial(int(x)),
            '1/x': lambda x: 1 / float(x),
            'abs': lambda x: abs(float(x)),
        }

        for func in func_map:
            while func in expr:
                start = expr.index(func)
                end = self.find_closing_parenthesis(expr, start + len(func))
                inside = expr[start + len(func) + 1:end]
                val = func_map[func](self.evaluate(inside))
                expr = expr[:start] + str(val) + expr[end + 1:]

        # Handle mod manually
        if 'mod' in expr:
            parts = expr.split('mod')
            if len(parts) == 2:
                return float(parts[0]) % float(parts[1])

        # Final simple evaluation (only basic math at this point)
        return self.simple_eval(expr)

    def find_closing_parenthesis(self, expr, start_idx):
        count = 1
        for i in range(start_idx + 1, len(expr)):
            if expr[i] == '(':
                count += 1
            elif expr[i] == ')':
                count -= 1
            if count == 0:
                return i
        raise ValueError("Unbalanced parentheses")

    def simple_eval(self, expr):
        import ast
        import operator as op

        # Supported operations
        operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
            ast.USub: op.neg
        }

        def eval_node(node):
            if isinstance(node, ast.Num):  # <number>
                return node.n
            elif isinstance(node, ast.BinOp):  # <left> <op> <right>
                return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
            elif isinstance(node, ast.UnaryOp):  # -<operand>
                return operators[type(node.op)](eval_node(node.operand))
            else:
                raise TypeError(node)

        expr_ast = ast.parse(expr, mode='eval')
        return eval_node(expr_ast.body)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScientificCalculator()
    window.show()
    sys.exit(app.exec_())
