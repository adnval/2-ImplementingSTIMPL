from stimpl.expression import BooleanLiteral
from stimpl.robustness import run_stimpl_robustness_tests
from stimpl.test import run_stimpl_sanity_tests
from stimpl.test_state import test_state_implementation

if __name__=='__main__':
  test_state_implementation()
  run_stimpl_sanity_tests()
  run_stimpl_robustness_tests()
