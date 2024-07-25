from stimpl.runtime import run_stimpl
from stimpl.expression import *
from stimpl.types import *
from stimpl.errors import *


class TestingError(Exception):
    def __init__(self, expected, actual):
        error_msg = f"{actual}  does not match {expected}"
        super().__init__(error_msg)


class TestingLiteralError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

    def __repr__(self):
        return "TestingLiteralError"


def check_equal(expected, actual):
    if expected != actual:
        raise TestingError(expected, actual)


def check_program_raises(raise_type, program):
    try:
        run_stimpl(program)
    except Exception as e:
        # This is supposed to raise something
        # with the same type as `raise_type`.
        if type(e) != type(raise_type):
            # There was another type of error raised.
            # Let's just reraise that.
            raise TestingLiteralError(f"Expected {raise_type} but got {e}.")
        else:
            # When it does, we are happy!
            return
    raise TestingLiteralError(f"Should have raised {raise_type}")


def check_run_result(expected, actual):
    expected_value, expected_type, _ = expected
    actual_value, actual_type, _ = actual
    if (expected_value, expected_type) != (actual_value, actual_type):
        raise TestingError((expected_value, expected_type),
                           (actual_value, actual_type))


def run_stimpl_sanity_tests():
    try:
        # Mathematical Expressions (5 pts)
        program = Add(IntLiteral(10), IntLiteral(10))
        check_run_result((20, Integer(), None), run_stimpl(program))

        program = Add(IntLiteral(20), IntLiteral(-10))
        check_run_result((10, Integer(), None), run_stimpl(program))

        program = Add(FloatingPointLiteral(5.5), FloatingPointLiteral(2.0))
        check_run_result((7.5, FloatingPoint(), None), run_stimpl(program))

        program = Subtract(IntLiteral(10), IntLiteral(10))
        check_run_result((0, Integer(), None), run_stimpl(program))

        program = Subtract(IntLiteral(10), IntLiteral(20))
        check_run_result((-10, Integer(), None), run_stimpl(program))

        program = Subtract(FloatingPointLiteral(5.5),
                           FloatingPointLiteral(2.0))
        check_run_result((3.5, FloatingPoint(), None), run_stimpl(program))

        program = Multiply(IntLiteral(10), IntLiteral(10))
        check_run_result((100, Integer(), None), run_stimpl(program))

        program = Multiply(FloatingPointLiteral(5.5),
                           FloatingPointLiteral(2.0))
        check_run_result((11.0, FloatingPoint(), None), run_stimpl(program))

        program = Divide(IntLiteral(10), IntLiteral(10))
        check_run_result((1, Integer(), None), run_stimpl(program))

        program = Divide(FloatingPointLiteral(
            10.0), FloatingPointLiteral(20.0))
        check_run_result((0.5, FloatingPoint(), None), run_stimpl(program))

        # Mathematical Expression Errors (5 pts)
        program = Add(FloatingPointLiteral(1.0), IntLiteral(1))
        check_program_raises(InterpTypeError(), program)
        program = Add(IntLiteral(1), FloatingPointLiteral(1.0))
        check_program_raises(InterpTypeError(), program)
        program = Add(BooleanLiteral(True), BooleanLiteral(True))
        check_program_raises(InterpTypeError(), program)
        program = Add(Ren(), Ren())
        check_program_raises(InterpTypeError(), program)

        program = Subtract(FloatingPointLiteral(1.0), IntLiteral(1))
        check_program_raises(InterpTypeError(), program)
        program = Subtract(IntLiteral(1), FloatingPointLiteral(1.0))
        check_program_raises(InterpTypeError(), program)
        program = Subtract(BooleanLiteral(True), BooleanLiteral(True))
        check_program_raises(InterpTypeError(), program)
        program = Subtract(Ren(), Ren())
        check_program_raises(InterpTypeError(), program)

        program = Multiply(FloatingPointLiteral(1.0), IntLiteral(1))
        check_program_raises(InterpTypeError(), program)
        program = Multiply(IntLiteral(1), FloatingPointLiteral(1.0))
        check_program_raises(InterpTypeError(), program)
        program = Multiply(BooleanLiteral(True), BooleanLiteral(True))
        check_program_raises(InterpTypeError(), program)
        program = Multiply(Ren(), Ren())
        check_program_raises(InterpTypeError(), program)

        program = Divide(FloatingPointLiteral(1.0), IntLiteral(1))
        check_program_raises(InterpTypeError(), program)
        program = Divide(IntLiteral(1), FloatingPointLiteral(1.0))
        check_program_raises(InterpTypeError(), program)
        program = Divide(BooleanLiteral(True), BooleanLiteral(True))
        check_program_raises(InterpTypeError(), program)
        program = Divide(Ren(), Ren())
        check_program_raises(InterpTypeError(), program)

        program = Divide(IntLiteral(1), IntLiteral(0))
        check_program_raises(InterpMathError(), program)
        program = Divide(FloatingPointLiteral(1.0), FloatingPointLiteral(0.0))
        check_program_raises(InterpMathError(), program)

        # String concatenation (5 pts)
        program = Add(StringLiteral("Hello"), StringLiteral(", World"))
        check_run_result(("Hello, World", String(), None), run_stimpl(program))

        # String concatenation errors (5 pts)
        program = Subtract(StringLiteral("Hello"), StringLiteral(", World"))
        check_program_raises(InterpTypeError(), program)

        program = Multiply(StringLiteral("Hello"), StringLiteral(", World"))
        check_program_raises(InterpTypeError(), program)

        program = Divide(StringLiteral("Hello"), StringLiteral(", World"))
        check_program_raises(InterpTypeError(), program)

        # Boolean/Relational Expressions (5 pts)
        program = And(BooleanLiteral(True), BooleanLiteral(True))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = And(BooleanLiteral(True), BooleanLiteral(False))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = And(BooleanLiteral(False), BooleanLiteral(False))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = And(BooleanLiteral(False), BooleanLiteral(True))
        check_run_result((False, Boolean(), None), run_stimpl(program))

        program = Or(BooleanLiteral(True), BooleanLiteral(True))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Or(BooleanLiteral(True), BooleanLiteral(False))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Or(BooleanLiteral(False), BooleanLiteral(False))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Or(BooleanLiteral(False), BooleanLiteral(True))
        check_run_result((True, Boolean(), None), run_stimpl(program))

        program = Not(BooleanLiteral(True))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Not(BooleanLiteral(False))
        check_run_result((True, Boolean(), None), run_stimpl(program))

        program = Lt(Ren(), Ren())
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Lt(BooleanLiteral(False), BooleanLiteral(True))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Lt(IntLiteral(10), IntLiteral(12))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Lt(FloatingPointLiteral(10.0), FloatingPointLiteral(12.0))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Lt(StringLiteral("alpha"), StringLiteral("beta"))
        check_run_result((True, Boolean(), None), run_stimpl(program))

        program = Lte(Ren(), Ren())
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Lte(BooleanLiteral(True), BooleanLiteral(True))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Lte(IntLiteral(12), IntLiteral(12))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Lte(FloatingPointLiteral(12.0), FloatingPointLiteral(12.0))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Lte(StringLiteral("beta"), StringLiteral("beta"))
        check_run_result((True, Boolean(), None), run_stimpl(program))

        program = Eq(Ren(), Ren())
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Eq(BooleanLiteral(True), BooleanLiteral(True))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Eq(IntLiteral(12), IntLiteral(12))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Eq(FloatingPointLiteral(12.0), FloatingPointLiteral(12.0))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Eq(StringLiteral("beta"), StringLiteral("beta"))
        check_run_result((True, Boolean(), None), run_stimpl(program))

        program = Ne(Ren(), Ren())
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Ne(BooleanLiteral(True), BooleanLiteral(True))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Ne(IntLiteral(12), IntLiteral(12))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Ne(FloatingPointLiteral(12.0), FloatingPointLiteral(12.0))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Ne(StringLiteral("beta"), StringLiteral("beta"))
        check_run_result((False, Boolean(), None), run_stimpl(program))

        program = Gt(Ren(), Ren())
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Gt(BooleanLiteral(False), BooleanLiteral(True))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Gt(IntLiteral(10), IntLiteral(12))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Gt(FloatingPointLiteral(10.0), FloatingPointLiteral(12.0))
        check_run_result((False, Boolean(), None), run_stimpl(program))
        program = Gt(StringLiteral("alpha"), StringLiteral("beta"))
        check_run_result((False, Boolean(), None), run_stimpl(program))

        program = Gte(Ren(), Ren())
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Gte(BooleanLiteral(True), BooleanLiteral(True))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Gte(IntLiteral(12), IntLiteral(12))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Gte(FloatingPointLiteral(12.0), FloatingPointLiteral(12.0))
        check_run_result((True, Boolean(), None), run_stimpl(program))
        program = Gte(StringLiteral("beta"), StringLiteral("beta"))
        check_run_result((True, Boolean(), None), run_stimpl(program))

        # Boolean Expression errors (5 pts)
        program = And(BooleanLiteral(True), IntLiteral(10))
        check_program_raises(InterpTypeError(), program)
        program = And(IntLiteral(10), BooleanLiteral(True))
        check_program_raises(InterpTypeError(), program)
        program = And(IntLiteral(10), IntLiteral(10))
        check_program_raises(InterpTypeError(), program)
        program = And(Ren(), Ren())
        check_program_raises(InterpTypeError(), program)

        program = Or(BooleanLiteral(True), IntLiteral(10))
        check_program_raises(InterpTypeError(), program)
        program = Or(IntLiteral(10), BooleanLiteral(True))
        check_program_raises(InterpTypeError(), program)
        program = Or(IntLiteral(10), IntLiteral(10))
        check_program_raises(InterpTypeError(), program)
        program = Or(Ren(), Ren())
        check_program_raises(InterpTypeError(), program)

        program = Not(IntLiteral(10))
        check_program_raises(InterpTypeError(), program)
        program = Not(FloatingPointLiteral(10.0))
        check_program_raises(InterpTypeError(), program)
        program = Not(StringLiteral("string"))
        check_program_raises(InterpTypeError(), program)
        program = Not(Ren())
        check_program_raises(InterpTypeError(), program)

        # Basic expression/sequence evaluation
        program = Program(IntLiteral(1), IntLiteral(2), IntLiteral(3))
        check_run_result((3, Integer(), None), run_stimpl(program))

        program = Program()
        check_run_result((None, Unit(), None), run_stimpl(program))

        # Basic variable read/write
        program = Program(Assign(Variable("i"), Ren()), Variable("i"))
        check_run_result((None, Unit(), None), run_stimpl(program))

        program = Program(Assign(Variable("i"), IntLiteral(1)), Variable("i"))
        check_run_result((1, Integer(), None), run_stimpl(program))

        program = Program(
            Assign(Variable("i"), FloatingPointLiteral(1.0)), Variable("i"))
        check_run_result((1, FloatingPoint(), None), run_stimpl(program))

        program = Program(
            Assign(Variable("i"), StringLiteral("test")), Variable("i"))
        check_run_result(("test", String(), None), run_stimpl(program))

        program = Program(
            Assign(Variable("i"), BooleanLiteral(True)), Variable("i"))
        check_run_result((True, Boolean(), None), run_stimpl(program))

        # Syntax error handling (5 pts)

        # Runtime syntax error to read from a variable before assignment
        program = Program(Variable("i"))
        check_program_raises(InterpSyntaxError(), program)

        # Assigning to something that is not a variable is a compile-
        # time syntax error.
        try:
            program = Assign(IntLiteral(10), IntLiteral(10))
        except Exception as e:
            if not isinstance(e, InterpSyntaxError):
                raise e
        # Make sure that sequences work in the proper order (10 pts)
        # i = 0
        # j = (i = i + 1)
        # k = (i = i + 1)
        # l = (i = i + 1)
        program = Program(
            Assign(Variable("i"), IntLiteral(0)),
            Assign(Variable("j"), Assign(Variable("i"),
                   Add(Variable("i"), IntLiteral(1)))),
            Assign(Variable("k"), Assign(Variable("i"),
                   Add(Variable("i"), IntLiteral(1)))),
            Assign(Variable("l"), Assign(Variable("i"),
                   Add(Variable("i"), IntLiteral(1)))),
        )
        run_value, run_type, run_state = run_stimpl(program)
        check_equal((1, Integer()), run_state.get_value("j"))
        check_equal((2, Integer()), run_state.get_value("k"))
        check_equal((3, Integer()), run_state.get_value("l"))
        check_equal((3, Integer()), run_state.get_value("i"))

        # Check If expression implementation (10 pts)
        # Check value of if expressions
        program = If(BooleanLiteral(False),
                     StringLiteral("Then"),
                     StringLiteral("Else"))
        check_run_result(("Else", String(), None), run_stimpl(program))

        program = If(BooleanLiteral(True),
                     StringLiteral("Then"),
                     StringLiteral("Else"))
        check_run_result(("Then", String(), None), run_stimpl(program))

        program = If(BooleanLiteral(False),
                     StringLiteral("Then"),
                     Ren())
        check_run_result((None, Unit(), None), run_stimpl(program))

        # Check whether If expression condition must be a Boolean.
        program = If(IntLiteral(1),
                     Variable("i"),
                     Variable("i"))
        check_program_raises(InterpTypeError(), program)

        # Check whether If expression condition can have side-effects.
        program = If(Ne(IntLiteral(0), Assign(Variable("i"), IntLiteral(10))),
                     Variable("i"),
                     Variable("i"))
        check_run_result((10, Integer(), None), run_stimpl(program))

        program = If(Eq(IntLiteral(0), Assign(Variable("i"), IntLiteral(10))),
                     Variable("i"),
                     Variable("i"))
        check_run_result((10, Integer(), None), run_stimpl(program))

        # Check to make sure that If bodies can have side effects.
        program = Assign(Variable("i"),
                         If(And(BooleanLiteral(False), BooleanLiteral(True)),
                            Assign(Variable("j"), StringLiteral("Then")),
                            Assign(Variable("j"), StringLiteral("Else"))),
                         )
        check_run_result(("Else", String(), None), run_stimpl(program))
        run_value, run_type, run_state = run_stimpl(program)
        check_equal(("Else", String()), run_state.get_value("j"))
        check_equal(("Else", String()), run_state.get_value("i"))

        # Make sure that While loops work! (10 pts)
        # Generic While loop
        program = Program(
            Assign(Variable("j"), IntLiteral(0)),
            While(Lt(Variable("j"), IntLiteral(10)),
                  Sequence(
                Assign(Variable("j"), Add(Variable("j"), IntLiteral(1))),
            )
            )
        )
        run_value, run_type, run_state = run_stimpl(program)
        check_equal((10, Integer()), run_state.get_value("j"))

        # While loop with non-Boolean condition should raise InterpTypeError
        program = Program(
            Assign(Variable("j"), IntLiteral(0)),
            While(IntLiteral(10),
                  Sequence(
                Assign(Variable("j"), Add(Variable("j"), IntLiteral(1))),
            )
            )
        )
        check_program_raises(InterpTypeError(), program)

        # Once a variable is assigned, its type is fixed. Check
        # to make sure that reassigning to a value with a different
        # type causes a type error to be raised. (5 pts)
        program = Program(
            Assign(Variable("i"), IntLiteral(10)),
            Assign(Variable("i"), FloatingPointLiteral(10.0))
        )
        check_program_raises(InterpTypeError(), program)

        program = Program(
            Assign(Variable("i"), Ren()),
            Assign(Variable("i"), FloatingPointLiteral(10.0))
        )
        check_program_raises(InterpTypeError(), program)

        # Check to make sure that you can use assignments as expressions
        # and that they propagate! (5 pts)
        # i = j = 10
        program = Assign(Variable("i"), Assign(Variable("j"), IntLiteral(10)))
        run_value, run_type, run_state = run_stimpl(program)
        check_equal((10, Integer()), run_state.get_value("i"))
        check_equal((10, Integer()), run_state.get_value("j"))

        # Check to make sure that side effects are allowed by operations. (5 pts)

        # (i = 10) + (i + (j = 11))
        # i = 10
        # j = 11
        # result = 10 + (10 + 11) = 31
        program = Add(Assign(Variable("i"), IntLiteral(10)), Add(
            Variable("i"), Assign(Variable("j"), IntLiteral(11))))
        run_value, run_type, run_state = run_stimpl(program)
        check_equal((31, Integer()), (run_value, run_type))
        check_equal((10, Integer()), run_state.get_value("i"))
        check_equal((11, Integer()), run_state.get_value("j"))

        # (i = 10) - (i + (j = 11))
        # i = 10
        # j = 11
        # result = 10 - (10 + 11) = -11
        program = Subtract(Assign(Variable("i"), IntLiteral(10)), Add(
            Variable("i"), Assign(Variable("j"), IntLiteral(11))))
        run_value, run_type, run_state = run_stimpl(program)
        check_equal((-11, Integer()), (run_value, run_type))
        check_equal((10, Integer()), run_state.get_value("i"))
        check_equal((11, Integer()), run_state.get_value("j"))

        # (i = 10) * (i + (j = 11))
        # i = 10
        # j = 11
        # result = 10 * (10 + 11) = 210
        program = Multiply(Assign(Variable("i"), IntLiteral(10)), Add(
            Variable("i"), Assign(Variable("j"), IntLiteral(11))))
        run_value, run_type, run_state = run_stimpl(program)
        check_equal((210, Integer()), (run_value, run_type))
        check_equal((10, Integer()), run_state.get_value("i"))
        check_equal((11, Integer()), run_state.get_value("j"))

        # (i = 10) / (i + (j = 10))
        # i = 10
        # j = 10
        # result = 10 / (10 + 10) = 0
        program = Divide(Assign(Variable("i"), IntLiteral(10)), Add(
            Variable("i"), Assign(Variable("j"), IntLiteral(10))))
        run_value, run_type, run_state = run_stimpl(program)
        check_equal((0, Integer()), (run_value, run_type))
        check_equal((10, Integer()), run_state.get_value("i"))
        check_equal((10, Integer()), run_state.get_value("j"))

    except Exception as e:
        raise e

    print("All (sanity) tests ran successfully!")
