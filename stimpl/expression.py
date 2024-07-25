from stimpl.errors import InterpSyntaxError, InterpTypeError, pretty_type
"""
Expressions
"""


class Expr(object):
    def __init__(self):
        pass


"""
Unit expression.
"""


class Ren(Expr):
    def __init__(self):
        pass

    def __repr__(self):
        return f"Ren value"


"""
Literal expressions.
"""


class Literal(Expr):
    def __init__(self, literal):
        self.literal = literal

    def __repr__(self):
        return f"literal value: {self.literal}"


class IntLiteral(Literal):
    def __init__(self, literal):
        if type(literal) != int:
            raise InterpTypeError(
                f"Integer literal cannot be {pretty_type(literal)}")
        super().__init__(literal)


class FloatingPointLiteral(Literal):
    def __init__(self, literal):
        if type(literal) != float:
            raise InterpTypeError(
                f"Floating-point literal cannot be {pretty_type(literal)}")
        super().__init__(literal)


class StringLiteral(Literal):
    def __init__(self, literal):
        if type(literal) != str:
            raise InterpTypeError(
                f"Integer literal cannot be {pretty_type(literal)}")
        super().__init__(literal)


class BooleanLiteral(Literal):
    def __init__(self, literal):
        if type(literal) != bool:
            raise InterpTypeError(
                f"Boolean literal cannot be {pretty_type(literal)}")
        super().__init__(literal)


"""
Variable Expression
"""


class Variable(Expr):
    def __init__(self, variable_name):
        self.variable_name = variable_name

    def __repr__(self):
        return f"Variable {self.variable_name}"

    def eval(self, state):
        return (state.get_value(self.variable_name), state)


"""
Operators
"""


class Assign(Expr):
    def __init__(self, variable, value):
        if not isinstance(variable, Variable):
            raise InterpSyntaxError("Must assign to a variable.")
        self.variable = variable
        self.value = value

    def __repr__(self):
        return f"{self.variable} = {self.value}"


class UnaryOperator(Expr):
    def __init__(self):
        super().__init__()


class Print(UnaryOperator):
    def __init__(self, to_print):
        self.to_print = to_print
        super().__init__()

    def __repr__(self):
        return f"Print {self.to_print}"


class Not(UnaryOperator):
    def __init__(self, expr):
        self.expr = expr
        super().__init__()

    def __repr__(self):
        return f"Not {self.expr}"


class BinaryOperator(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        super().__init__()


class And(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} && {self.right}"


class Or(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} || {self.right}"


class Lt(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} < {self.right}"


class Lte(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} <= {self.right}"


class Gt(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} > {self.right}"


class Gte(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} >= {self.right}"


class Eq(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} == {self.right}"


class Ne(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} != {self.right}"


class Add(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} + {self.right}"


class Subtract(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} - {self.right}"


class Multiply(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} * {self.right}"


class Divide(BinaryOperator):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"{self.left} / {self.right}"


"""
Combining forms.
"""


class Program(Expr):
    def __init__(self, *exprs):
        self.exprs = exprs

    def __repr__(self):
        exprs = self.exprs
        if len(exprs) == 0:
            exprs = ["None"]
        return "Program: " + ";\n".join([repr(x) for x in exprs])


class Sequence(Expr):
    def __init__(self, *exprs):
        self.exprs = exprs

    def __repr__(self):
        exprs = self.exprs
        if len(exprs) == 0:
            exprs = ["None"]
        return "Sequence: " + ";\n".join([repr(x) for x in exprs])


class If(Expr):
    def __init__(self, condition, true, false):
        self.condition = condition
        self.true = true
        self.false = false

    def __repr__(self):
        return f"if ({self.condition}) then {{ {self.true} }} else {{ {self.false} }}"


class While(Expr):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"while ({self.condition}) {{ {self.body} }}"
