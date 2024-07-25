from stimpl.runtime import EmptyState
from stimpl.types import Boolean, Integer
from stimpl.test import check_equal

def test_state_implementation():
    state = EmptyState()
    check_equal(None, state.get_value("x")) 
    state2 = state.set_value("x", 5, Integer())
    check_equal((5, Integer()), state2.get_value("x")) 
    state3 = state2.set_value("k", True, Boolean())
    check_equal((True, Boolean()),state3.get_value("k"))
    state4 = state3.set_value("x", 7, Integer())
    check_equal((7, Integer()),state4.get_value("x"))
    check_equal((5, Integer()), state2.get_value("x"))
    check_equal(None,state4.get_value("y"))