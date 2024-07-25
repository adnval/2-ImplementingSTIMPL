"""
Types
"""


class Type(object):
    def __init__(self):
        pass


class Unit(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "Unit"

    def __eq__(self, other):
        match other:
            case Unit():
                return True
            case _:
                return False


class Integer(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "Integer"

    def __eq__(self, other):
        match other:
            case Integer():
                return True
            case _:
                return False


class FloatingPoint(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "FloatingPoint"

    def __eq__(self, other):
        match other:
            case FloatingPoint():
                return True
            case _:
                return False


class String(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "String"

    def __eq__(self, other):
        match other:
            case String():
                return True
            case _:
                return False


class Boolean(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "Boolean"

    def __eq__(self, other):
        match other:
            case Boolean():
                return True
            case _:
                return False
