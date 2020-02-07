import os
import sys

test_dir_path = os.path.dirname(os.path.realpath(__file__))
main_dir = os.path.dirname(test_dir_path)
sys.path.append(main_dir)
from flask_value_checker import (
    restrictions,
    ValueChecker,
    FlaskValueCheckerSyntaxError,
    FlaskValueCheckerValueError,
    Invigilator,
)
