import re
"""
Interpreter errors.
"""
class InterpError(Exception):
  def __init__(self, error_msg):
    error_msg = re.sub(r"[\n\s]+", ' ', error_msg)
    super().__init__(error_msg)

class InterpSyntaxError(InterpError):
  def __init__(self, error_msg = None):
    if error_msg == None:
      error_msg = "InterpSyntaxError"
    super().__init__(error_msg)

class InterpTypeError(InterpError):
  def __init__(self, error_msg = None):
    if error_msg == None:
      error_msg = "InterpTypeError"
    super().__init__(error_msg)

class InterpMathError(InterpError):
  def __init__(self, error_msg = None):
    if error_msg == None:
      error_msg = "InterpMathError"
    super().__init__(error_msg)

def pretty_type(value):
  return f"{str(type(value).__name__)}"
