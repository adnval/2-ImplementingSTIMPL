from typing import Any, Tuple, Optional

from stimpl.expression import *
from stimpl.types import *
from stimpl.errors import *

"""
Interpreter State
"""


class State(object):
    def __init__(self, variable_name: str, variable_value: Expr, variable_type: Type, next_state: 'State') -> None:
        self.variable_name = variable_name
        self.value = (variable_value, variable_type)
        self.next_state = next_state

    def copy(self) -> 'State':
        variable_value, variable_type = self.value
        return State(self.variable_name, variable_value, variable_type, self.next_state)

    def set_value(self, variable_name, variable_value, variable_type):
        return State(variable_name, variable_value, variable_type, self)

    def get_value(self, variable_name) -> Any:
        """
        Returns a tuple of the variable's value and type.
        """
        if variable_name == self.variable_name:
            return self.value
        if self.next_state is not None:
            return self.next_state.get_value(variable_name)
        return None

    def __repr__(self) -> str:
        return f"{self.variable_name}: {self.value}, " + repr(self.next_state)


class EmptyState(State):
    def __init__(self):
        pass

    def copy(self) -> 'EmptyState':
        return EmptyState()

    def get_value(self, variable_name) -> None:
        return None

    def __repr__(self) -> str:
        return ""


"""
Main evaluation logic!
"""


def evaluate(expression: Expr, state: State) -> Tuple[Optional[Any], Type, State]:
    match expression:
        case Ren():
            return (None, Unit(), state)

        case IntLiteral(literal=l):
            return (l, Integer(), state)

        case FloatingPointLiteral(literal=l):
            return (l, FloatingPoint(), state)

        case StringLiteral(literal=l):
            return (l, String(), state)

        case BooleanLiteral(literal=l):
            return (l, Boolean(), state)

        case Print(to_print=to_print):
            printable_value, printable_type, new_state = evaluate(to_print, state)

            match printable_type:
                case Unit():
                    print("Unit")
                case _:
                    print(f"{printable_value}")

            return (printable_value, printable_type, new_state)

        case Sequence(exprs=exprs) | Program(exprs=exprs):
            """
            Loops through each inputted expression and evaluates them
            """
            expr_value, expr_type, new_state = evaluate(Ren(), state)
            for expr in exprs:
                expr_value, expr_type, new_state = evaluate(expr, new_state)
            return (expr_value, expr_type, new_state)

        case Variable(variable_name=variable_name):
            value = state.get_value(variable_name)
            if value == None:
                raise InterpSyntaxError(f"Cannot read from {variable_name} before assignment.")
            variable_value, variable_type = value
            return (variable_value, variable_type, state)

        case Assign(variable=variable, value=value):

            value_result, value_type, new_state = evaluate(value, state)

            variable_from_state = new_state.get_value(variable.variable_name)
            _, variable_type = variable_from_state if variable_from_state else (None, None)

            if value_type != variable_type and variable_type != None:
                raise InterpTypeError(f"""Mismatched types for Assignment: Cannot assign {value_type} to {variable_type}""")

            new_state = new_state.set_value(variable.variable_name, value_result, value_type)
            return (value_result, value_type, new_state)

        case Add(left=left, right=right):
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Add: Cannot add {left_type} to {right_type}""")

            match left_type:
                case Integer() | String() | FloatingPoint():
                    result = left_result + right_result
                case _:
                    raise InterpTypeError(f"""Cannot add {left_type}s""")

            return (result, left_type, new_state)

        case Subtract(left=left, right=right):
            """
            Returns the result of the subtraction operation.
            """
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for subtract: Cannot subtract {left_type} to {right_type}""")

            match left_type:
                case Integer() | FloatingPoint(): # Type checking
                    result = left_result - right_result
                case _: # Any other types are not compatible
                    raise InterpTypeError(f"""Cannot subtract {left_type}s""")

            return (result, left_type, new_state)

        case Multiply(left=left, right=right):
            """
            Returns the result of the multiplication operation.
            """
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for multiply: Cannot multiply {left_type} to {right_type}""")

            match left_type:
                case Integer() | FloatingPoint(): # Type checking
                    result = left_result * right_result
                case _: # Any other types are not compatible
                    raise InterpTypeError(f"""Cannot multiply {left_type}s""")

            return (result, left_type, new_state)

        case Divide(left=left, right=right):
            """
            Returns the result of the division operation.
            """
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for divide: Cannot divide {left_type} to {right_type}""")

            if right_result == 0: # Ensures that division by zero raises a MathError
                raise InterpMathError(f"""Math error for divide: Cannot divide by zero""")

            match left_type: # Type checking
                case Integer():
                    result = left_result // right_result # Ensures integer division
                case FloatingPoint():
                    result = left_result / right_result
                case _: # Any other types are not compatible
                    raise InterpTypeError(f"""Cannot divide {left_type}s""")

            return (result, left_type, new_state)

        case And(left=left, right=right):
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for And: Cannot evaluate {left_type} and {right_type}""")
            match left_type:
                case Boolean():
                    result = left_value and right_value
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical and on non-boolean operands.")

            return (result, left_type, new_state)

        case Or(left=left, right=right):
            """
            Returns the boolean result of the or operation.
            """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for Or: Cannot evaluate {left_type} or {right_type}""")
            match left_type:
                case Boolean(): # Type checking
                    result = left_value or right_value
                case _: # Any other types are not compatible
                    raise InterpTypeError(
                        "Cannot perform logical or on non-boolean operands.")

            return (result, left_type, new_state)

        case Not(expr=expr):
            """
            Returns the inverse of the inputted expression.
            """
            expr_value, expr_type, new_state = evaluate(expr, state)
            match expr_type:
                case Boolean(): # Type checking
                    result = not(expr_value)
                case _: # Any other types are not compatible
                    raise InterpTypeError("Cannot perform logical not on a non-boolean operand.")
            return (result, expr_type, new_state)

        case If(condition=condition, true=true, false=false):
            """
            Returns the result of the conditional.
            """
            cond_result, cond_type, new_state = evaluate(condition, state)
            match cond_type:
                case Boolean(): # Type checking
                    result = cond_result
                case _: # Any other types are not compatible
                    raise InterpTypeError("Cannot perform conditional on a non-boolean operand.")
            return evaluate(true, new_state) if result else evaluate(false, new_state) # Returns true if the result of the condition is true, otherwise false

        case Lt(left=left, right=right):
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value < right_value
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(
                        f"Cannot perform < on {left_type} type.")

            return (result, Boolean(), new_state)

        case Lte(left=left, right=right):
            """
            Returns the result of the less than or equal to operation.
            """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for Lte: Cannot compare {left_type} and {right_type}""")

            match left_type: # Type checking
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value <= right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(f"Cannot perform <= on {left_type} type.")
            return (result, Boolean(), new_state)

        case Gt(left=left, right=right):
            """
            Returns the result of the greater than operation.
            """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type: # Ensures the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for Gt: Cannot compare {left_type} and {right_type}""")

            match left_type: # Type checking
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value > right_value
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(f"Cannot perform > on {left_type} type.")
            return (result, Boolean(), new_state)

        case Gte(left=left, right=right):
            """
            Returns the result of the greater than or equal to operation.
            """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for Gte: Cannot compare {left_type} and {right_type}""")

            match left_type: # Type checking
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value >= right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(f"Cannot perform >= on {left_type} type.")
            return (result, Boolean(), new_state)

        case Eq(left=left, right=right):
            """
            Returns the result of the equal to operation.
            """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for Eq: Cannot compare {left_type} and {right_type}""")

            match left_type: # Type checking
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value == right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(f"Cannot perform == on {left_type} type.")
            return (result, Boolean(), new_state)

        case Ne(left=left, right=right):
            """
            Returns the result of the not equals to operation.
            """
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            if left_type != right_type: # Ensures that the types of both sides are the same
                raise InterpTypeError(f"""Mismatched types for Ne: Cannot compare {left_type} and {right_type}""")

            match left_type: # Type checking
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value != right_value
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(f"Cannot perform != on {left_type} type.")
            return (result, Boolean(), new_state)

        case While(condition=condition, body=body):
            """
            Returns the result of the while loop
            """
            cond_result, cond_type, new_state = evaluate(condition, state)
            match cond_type: # Type checking the conditional
                case Boolean():
                    result = cond_result
                case _:
                    raise InterpTypeError("Condition expression must have a boolean type")
            while result: # While the condition is true...
                body_result, body_type, new_state = evaluate(body, new_state)
                cond_result, cond_type, new_state = evaluate(condition, new_state)
                match cond_type: # Additional type checking for the conditional
                    case Boolean():
                        result = cond_result
                    case _:
                        raise InterpTypeError("Condition expression must have a boolean type")
            return (result, cond_type, new_state)
        case _:
            raise InterpSyntaxError("Unhandled!")
    pass


def run_stimpl(program, debug=False):
    state = EmptyState()
    program_value, program_type, program_state = evaluate(program, state)

    if debug:
        print(f"program: {program}")
        print(f"final_value: ({program_value}, {program_type})")
        print(f"final_state: {program_state}")

    return program_value, program_type, program_state
