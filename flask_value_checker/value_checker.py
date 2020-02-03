"""
all the code behind the 'check_values_exist' decorator
"""
from functools import wraps
from flask import jsonify, request, Response
from .value_checker_class import ValueChecker

import json
from .restrictions import errors
from . import restrictions
import textwrap


def check_values_exist(check_for_method, value):
    '''
    check if values exist if the method is followed,
    NOTE: if any other method is followed, does not raise
          an error

    Parameters
    ----------
    check_for_method : str
        the method to check parameters

    value : str
        check strings, must be in the format mentioned

    HTTP-Returns
    ------------
    400
        on failure, the response will be similar to,

        {
            "error": {
                "code": "MALFORMED_OR_MISSING_PARAMETERS",
                "message": "one or more fields we're either missing or malformed",
                "fields": {
                    "email" : "missing parameter, parameter is required",
                    "firstName" : "name has to be under 15 characters",
                    "age" : "parameter has to be of type 'int'"
                }
            }
        }

    *
        or whatever the original function returns

        *


    Example
    -------
    >>> @app.route('/abc')
    ... @check_values_exist(
    ...     'POST', """
    ...     firstName : str/length_range(0, 18)/required
    ...     middleName : str
    ...     lastName : str
    ...     email : str/required
    ...     password : str/length_range(8, 25)/required
    ...     phone : str/length_range(8, 25)/required
    ...     age : int/range(18, 999)
    ...     password : str/length_range(8, 25)/required
    ...     height : float/range(1, 11)
    ...     """
    ... )
    ... def abc():
    ...     ...
    ...     ...
    '''
    checker = ValueChecker(value)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.method == check_for_method:
                return f(*args, **kwargs)

            has_errors, final_message = checker.check()

            if has_errors:
                return Response(
                    json.dumps(final_message), status=400, mimetype="application/json"
                )
            else:
                return f(*args, **kwargs)

        return wrapper

    return decorator
