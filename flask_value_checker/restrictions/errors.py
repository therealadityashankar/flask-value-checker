class FlaskValueCheckerError(Exception):
    """base flask value checker error"""

    pass


class FlaskValueCheckerSyntaxError(FlaskValueCheckerError):
    """
    for syntactic errors
    """

    pass


class FlaskValueCheckerValueError(ValueError):
    """
    value error for flask value checker
    """

    pass
