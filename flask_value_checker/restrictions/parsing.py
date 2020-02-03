from .restrictions import *
from . import errors


def make_restriction(raw_line: str):
    """
    make a restriction, depending on the line

    lines must not have comments, and must have a restriction in
    the string format

    Returns
    -------
    like str, GenericRestriction
        if parameter is present,
    else
        None, None
    """
    original_raw_line = raw_line
    raw_line = clean_code_line(raw_line)
    if raw_line == "":
        return None, None

    restriction_classes = get_restriction_classes()
    parameter, type_str, attrs = get_details_from_raw_restriction(raw_line)
    for R_class in restriction_classes:
        if R_class.type_keyword == type_str:
            checker = R_class(original_raw_line, parameter, attrs)
            break
    else:
        known_value_types = [r.type_keyword for r in restriction_classes]
        raise errors.FlaskValueCheckerValueError(
            textwrap.dedent(
                f"""\
        unknown value type {type_str},
        please choose a value type out of {known_value_types}

        Error in line:
        {raw_line}
        """
            )
        )

    return parameter, checker


def make_restrictions(raw_lines: str):
    raw_lines = raw_lines.split("\n")
    checkers = {}

    for line in raw_lines:
        parameter, checker = make_restriction(line)
        if parameter:
            checkers[parameter] = checker

    return checkers


def clean_code_line(raw_line: str):
    """
    remove comments and spaces from code line
    """
    try:
        comment_start = raw_line.index("#")
        raw_line = raw_line[:comment_start]
    except ValueError:
        pass

    raw_line = raw_line.strip()
    return raw_line


def get_details_from_raw_restriction(raw_line: str):
    line = raw_line.strip()
    args = line.split(":")

    if len(args) != 2:
        raise errors.FlaskValueCheckerSyntacticError(
            textwrap.dedent(
                f"""\
        the value checker format restricts exactly one `:` per line,
        error in line -
        {raw_line}"""
            )
        )

    parameter, restrictions_raw = args
    parameter = parameter.strip()
    restrictions_raw = restrictions_raw.strip()
    restriction_vals = restrictions_raw.split("/")
    restriction_vals = [restriction_val.strip() for restriction_val in restriction_vals]
    res_type = restriction_vals[0]
    attrs = restriction_vals[1:]
    return parameter, res_type, attrs
