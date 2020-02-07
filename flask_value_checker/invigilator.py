from functools import wraps
from flask import jsonify, request, Response, g
from .value_checker import ValueChecker

import json
from .restrictions import errors
from . import restrictions


class Invigilator:
    """
    lets check how your form/query parameters are, kay ?
    """

    def __init__(self, err_handler=None):
        """
        create an Invigilator

        Parameters
        ----------
        err_handler : function
            the errors are passed into this function as
            a parameter

            the return part of this function works similar
            to most flask routes
        """
        if err_handler is None:

            def err_handler(errs):
                """
                default err handler
                """
                error = {
                    "error": {
                        "code": "MALFORMED_OR_MISSING_PARAMETERS",
                        "message": "one or more fields we're either missing or malformed",
                        "fields": errs,
                    }
                }
                error = json.dumps(error)
                return Response(error, status=400, mimetype="application/json")

        self.err_handler = err_handler

    def check(self, check_for_method, value):
        '''
        check if values exist if the method is followed,
        NOTE: if any other method is followed, does not raise
              an error

        Parameters
        ----------
        check_for_method : str or list of strs
            the method to check for or the methods to
            check for

        value : str
            check strings, must be in the format mentioned

        HTTP-Returns
        ------------
        400
            *
                if you've a custom error handler

            default error handler is similar to:

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
        >>> invigilator = Invigilator()
        >>> @app.route('/abc')
        ... @invigilator.check(
        ...     'POST',
        ...     """
        ...     firstName : str/lenlim(0, 18)
        ...     middleName : str/optional
        ...     lastName : str/optional
        ...     email : str
        ...     password : str/lenlim(8, 25)
        ...     phone : str/lenlim(8, 25)
        ...     age : int/range(18, 999)
        ...     password : str/lenlim(8, 25)
        ...     height : float/range(1, 11)
        ...     """
        ... )
        ... def abc():
        ...     ...
        ...     ...
        '''
        if isinstance(check_for_method, str):
            check_for_method = [check_for_method]

        checker = ValueChecker(value)

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                g.value_checker = checker
                if not request.method in check_for_method:
                    return f(*args, **kwargs)

                errors = checker.check()

                if errors:
                    return self.err_handler(errors)
                else:
                    return f(*args, **kwargs)

            return wrapper

        return decorator
