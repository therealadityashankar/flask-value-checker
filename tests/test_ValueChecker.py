"""
TODO TESTS:
  - Syntax errors,
  - general tests
"""
from helper import (
    ValueChecker,
    FlaskValueCheckerSyntaxError,
    FlaskValueCheckerValueError,
)

import random
import string
import pytest

test_restriction_code = """
    # some simple data for tests here
    firstName : str/lenlim(5, 15) # a random comment
    middleName : str/lenlim(5, inf)/optional
    lastName : str/optional
    email : str
    password : str/lenlim(8, 15)
    phone : str/lenlim(8, 15)
    age : int/lim(18, 99)
    height : float/lim(1, inf)/optional
    someNegativeFloat : float/optional/lim(-inf, 0)
    team : str/accept(["red", "blue", "yellow", "green", "orange"])
    acceptTermsAndConditions : str/accept(['on'])/optional
    someEdgeCase : str/accept(['on'])
"""

checker = ValueChecker(test_restriction_code)

sample_test_dict = {
    "firstName": "Garyashver",
    "email": "GaryBob@Dan.com",
    "phone": "9120921022",
    "age": "76",
    "password": "12345678",
    "team": "red",
    "someEdgeCase": "on",
}


def create_sample_dict(modifications=None):
    modifications = {} if modifications is None else modifications
    test_dict = sample_test_dict.copy()
    for key, value in modifications.items():
        if value is None:
            if key in test_dict:
                del test_dict[key]
        else:
            test_dict[key] = value
    return test_dict


def run_tests_for_param(param, tests, pre_func=None):
    for test in tests:
        pre_value, expected_output = test
        if pre_func:
            value = pre_func(pre_value)
        else:
            value = pre_value

        test_dict = create_sample_dict({param: value})
        errs = checker.check_for(test_dict)

        bad_err_text = f"""
        param : {param},
        pre_value : {pre_value},
        value : {value},
        expected_output : {expected_output},
        """
        if expected_output is None:
            assert errs is None, bad_err_text
        else:
            assert errs[param] == expected_output, bad_err_text


def create_rand_text(length, max_len=None):
    """
    create random text for a specific length,
    if max_len is specified creates a random piece of text
    which is of a random length between length and max_len
    """
    if max_len is not None:
        length = random.randint(length, max_len)

    to_ret_string = ""

    for _ in range(length):
        to_ret_string += random.choice(string.printable)

    return to_ret_string


def test_simple_pass():
    error = checker.check_for(sample_test_dict)
    assert error is None


def test_simple_fail():
    test_dict = create_sample_dict({"age": None})
    errors = checker.check_for(test_dict)
    assert errors is not None

    fields = errors
    assert "age" in fields
    assert len(fields.items()) == 1


def test_optional_field():
    test_dict = create_sample_dict({"middleName": "sarah"})
    errors = checker.check_for(test_dict)
    assert errors is None

    test_dict = create_sample_dict({})
    errors = checker.check_for(test_dict)
    assert errors is None


def test_string_length_limits():
    def pre_func(val):
        if type(val) != tuple:
            val = (val,)

        return create_rand_text(*val)

    # tests are run on the modif_param
    modif_param = "firstName"
    invalid_range_err = "string length must be between 5 and 15"

    # tests represent parameters, text_len, expected_output_error
    tests = [
        [2, invalid_range_err],
        [3, invalid_range_err],
        [(0, 4), invalid_range_err],
        [5, None],
        [(5, 15), None],
        [(5, 15), None],
        [(16, 1000), invalid_range_err],
        [(16, 1000), invalid_range_err],
    ]

    run_tests_for_param(modif_param, tests, pre_func)

    # tests are run on the modif_param
    modif_param = "middleName"
    invalid_range_err = "string length must be between 5 and inf"

    # tests represent parameters, text_len, expected_output_error
    tests = [
        [2, invalid_range_err],
        [3, invalid_range_err],
        [(0, 4), invalid_range_err],
        [5, None],
        [(5, 15), None],
        [(5, 15), None],
        [(15, 1000), None],
        [(15, 1000), None],
    ]

    run_tests_for_param(modif_param, tests, pre_func)

    # tests are run on the modif_param
    modif_param = "lastName"
    invalid_range_err = ""

    # tests represent parameters, text_len, expected_output_error
    tests = [
        [2, None],
        [3, None],
        [(0, 4), None],
        [5, None],
        [(5, 15), None],
        [(5, 15), None],
        [(15, 1000), None],
        [(15, 1000), None],
    ]

    run_tests_for_param(modif_param, tests, pre_func)


def test_string_accept():
    modif_param = "team"
    invalid_value_error = (
        "value must be one from the list ['red', 'blue', 'yellow', 'green', 'orange']"
    )

    tests = [
        ["red", None],
        ["blue", None],
        ["Green", invalid_value_error],
        ["iojoidas", invalid_value_error],
        ["", invalid_value_error],
    ]

    run_tests_for_param(modif_param, tests)

    modif_param = "acceptTermsAndConditions"
    invalid_value_error = "value should be 'on', or the field should not be submitted"
    tests = [
        ["on", None],
        [None, None],
        ["avcdscs", invalid_value_error],
        ["", invalid_value_error],
    ]

    run_tests_for_param(modif_param, tests)

    modif_param = "someEdgeCase"
    invalid_value_error = "value should be 'on'"
    tests = [
        ["on", None],
        ["avcdscs", invalid_value_error],
        ["", invalid_value_error],
        [None, invalid_value_error],
    ]

    run_tests_for_param(modif_param, tests)


def test_int_limits():
    def pre_func(val):
        if type(val) != tuple:
            return val

        return random.randint(*val)

    # tests are run on the modif_param
    modif_param = "age"
    invalid_range_err = "value must be between 18.0 and 99.0"

    # tests represent parameters, text_len, expected_output_error
    tests = [
        [2, invalid_range_err],
        [3, invalid_range_err],
        [-4, invalid_range_err],
        [-7, invalid_range_err],
        [(-1000, 17), invalid_range_err],
        [18, None],  # edge case
        [(18, 99), None],
        [(18, 99), None],
        [99, None],  # edge case
        [(100, 1000), invalid_range_err],
        [(100, 1000), invalid_range_err],
    ]
    run_tests_for_param(modif_param, tests, pre_func)

    # tests are run on the modif_param
    modif_param = "height"
    invalid_range_err = "value must be between 1.0 and inf"

    # tests represent parameters, text_len, expected_output_error
    tests = [
        [1, None],  # edge case
        [2, None],
        [3, None],
        [-4, invalid_range_err],
        [-7, invalid_range_err],
        [(-10000, 0), invalid_range_err],
        [(15, 99), None],
        [(15, 99), None],
        [99, None],
        [(100, 10000), None],
        [(100, 10000), None],
    ]
    run_tests_for_param(modif_param, tests, pre_func)

    # tests are run on the modif_param
    modif_param = "someNegativeFloat"
    invalid_range_err = "value must be between -inf and 0.0"

    # tests represent parameters, text_len, expected_output_error
    tests = [
        [0, None],  # edge case
        [(-10000, 0), None],
        [(-10000, 0), None],
        [(100, 10000), invalid_range_err],
        [(100, 10000), invalid_range_err],
    ]
    run_tests_for_param(modif_param, tests, pre_func)


def test_bad_syntax():
    bad_syntax_1 = """
        middleName : str/lenlim(5, inf)/optional

        # bad syntax over here, end bracket is missing
        firstName : str/lenlim(5, 15

        lastName : str/optional
        email : str
        password : str/lenlim(8, 15)
        phone : str/lenlim(8, 15)
        age : int/lim(18, 99)
        height : float/lim(1, inf)/optional
        someNegativeFloat : float/optional/lim(-inf, 0)
    """
    with pytest.raises(FlaskValueCheckerSyntaxError):
        checker = ValueChecker(bad_syntax_1)

    bad_syntax_2 = """
        # bad syntax over here, 3 parameters instead of 2
        firstName : str/lenlim(5, 15, 56)
        middleName : str/lenlim(5, inf)/optional
        lastName : str/optional
        email : str
        password : str/lenlim(8, 15)
        phone : str/lenlim(8, 15)
        age : int/lim(18, 99)
        height : float/lim(1, inf)/optional
        someNegativeFloat : float/optional/lim(-inf, 0)
    """
    with pytest.raises(FlaskValueCheckerValueError):
        checker = ValueChecker(bad_syntax_2)

    bad_syntax_3 = """
        # bad syntax over here, 1 parameter instead of 2
        firstName : str/lenlim(5)
        middleName : str/lenlim(5, inf)/optional
        lastName : str/optional
        email : str
    """
    with pytest.raises(FlaskValueCheckerValueError):
        checker = ValueChecker(bad_syntax_3)

    bad_syntax_4 = """
        # bad parameter name here
        firstName : str/blablabla
        middleName : str/lenlim(5, inf)/optional
        lastName : str/optional
        email : str
    """
    with pytest.raises(FlaskValueCheckerValueError):
        checker = ValueChecker(bad_syntax_4)

    bad_syntax_5 = """
        # bad parameter name here
        firstName : str/accept([,])
        middleName : str/lenlim(5, inf)/optional
        lastName : str/optional
        email : str
    """
    with pytest.raises(FlaskValueCheckerSyntaxError):
        checker = ValueChecker(bad_syntax_5)

    bad_syntax_6 = """
        # bad parameter name here
        firstName : str/accept([abc)
        middleName : str/lenlim(5, inf)/optional
        lastName : str/optional
        email : str
    """
    with pytest.raises(FlaskValueCheckerSyntaxError):
        checker = ValueChecker(bad_syntax_6)

    bad_syntax_7 = """
        # bad parameter name here
        firstName : str/accept(["abc'])
        middleName : str/lenlim(5, inf)/optional
        lastName : str/optional
        email : str
    """
    with pytest.raises(FlaskValueCheckerSyntaxError):
        checker = ValueChecker(bad_syntax_7)

    bad_syntax_8 = """
        # bad parameter name here
        firstName : str/accept(["abc", 124])
        middleName : str/lenlim(5, inf)/optional
        lastName : str/optional
        email : str
    """
    with pytest.raises(FlaskValueCheckerValueError):
        checker = ValueChecker(bad_syntax_8)
