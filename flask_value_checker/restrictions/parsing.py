import textwrap
import string

from . import restrictions
from . import errors

NUMBER_VALID_VALS = string.digits + "-" + "inf"


def make_restrictions(raw_lines: str):
    raw_lines = raw_lines.split("\n")
    checkers = {}

    for line in raw_lines:
        rest_parser = RestrictionParser(line)
        if not (rest_parser.is_comment_line or rest_parser.is_empty_line):
            field_name, checker = rest_parser.get_appropriate_restriction()
            checkers[field_name] = checker

    return checkers


class RestrictionParser:
    """
    parser to parse flask-value-checker

    format <StringRestrictionText>:
        <parameter_name> : <attr>/<attr>/<attr>

    format <attr>:
        <attr_name>
        <attr_name>()
        <attr_name>(<val_1>, <val_2>, ...)

    format <val>:
        str, list, or
    """

    def __init__(self, raw_line):
        self.raw_line = raw_line
        self.curr_pos = 0

        self.field_name = None
        self.attrs = []

        self.is_comment_line = False

        if len(raw_line):
            self.is_empty_line = False
            self.parse()
        else:
            self.is_empty_line = True

    def get_appropriate_restriction(self):
        """
        get the appropriate restriction based on the
        first attribute
        """
        # ensure the first argument (i.e. type argument) has not parameters
        type_str, type_attrs = self.attrs[0]

        if type_attrs:
            raise errors.FlaskValueCheckerSyntaxError(
                textwrap.dedent(
                    f"""\
                    the type attribute should NOT have attributes,
                    (i.e. here, {type_str} should not have paranthesis, i.e.
                    the ({type_attrs}) part)
                    """
                )
            )

        r_attrs = self.attrs[1:]

        restriction_classes = restrictions.get_restriction_classes()

        for RClass in restriction_classes:
            if RClass.type_keyword == type_str:
                checker = RClass(self.raw_line, self.field_name, r_attrs)
                break
        else:
            known_value_types = [r.type_keyword for r in restriction_classes]
            raise errors.FlaskValueCheckerValueError(
                textwrap.dedent(
                    f"""\
            unknown value type {type_str},
            please choose a value type out of {known_value_types}

            Error in line:
            {self.raw_line}
            """
                )
            )

        return self.field_name, checker

    def parse(self):
        self.minus_space_gulper()
        if self.curr_char == "#":
            self.is_comment_line = True
        elif self.curr_char is None:
            self.is_empty_line = True
        else:
            self.set_field_name()
            self.minus_space_gulper()
            self.parse_attrs()

    @property
    def curr_char(self):
        try:
            return self.raw_line[self.curr_pos]
        except IndexError:
            return None

    def gulp_char(self):
        self.curr_pos += 1

    def minus_space_gulper(self):
        self.gulp_char()
        while self.curr_char == " ":
            self.gulp_char()

    def set_field_name(self):
        self.field_name = self.parse_variable()
        try:
            self.curr_pos = self.raw_line.index(":")
        except:
            self.raise_syntax_error(
                "there must be a `:`  to seperate the param and its attributes"
            )

    def parse_attrs(self):
        attr_just_found = False
        while True:
            if attr_just_found:
                if self.curr_char == "/":
                    attr_just_found = False
                    self.minus_space_gulper()
                elif self.curr_char is None or self.curr_char == "#":
                    break
                else:
                    self.raise_syntax_error(
                        f"attributes must end with a '/' or, \
    in case they are the last character, spaces or nothing,\
    or a '#' if its before a comment,\
    they should not end with a {self.curr_char}"
                    )

            else:
                attr = self.parse_attr()
                self.attrs.append(attr)
                attr_just_found = True

    def parse_attr(self):
        name = ""
        params = []

        if self.curr_char in string.ascii_lowercase:
            name = self.parse_variable()
        else:
            self.raise_syntax_error(
                "invalid attribute name (attributes can only start with a lower case letter)"
            )

        if self.curr_char == " ":
            self.minus_space_gulper()

        if self.curr_char == "(":
            params = self.parse_attr_params()

        if self.curr_char == " ":
            self.minus_space_gulper()

        if self.curr_char == "/" or self.curr_char == None or self.curr_char == "#":
            return name, params
        else:
            self.raise_syntax_error(
                f"attributes must end with a '/' or, \
in case they are the last character, spaces or nothing,\
or a '#' if its before a comment,\
they should not end with a {self.curr_char}"
            )

    def parse_attr_params(self):
        self.check_starting_character("(", "attribute parameter")
        # remove the first "("
        self.gulp_char()

        first_param = self.parse_attr_param()
        params = [first_param]

        while True:
            if self.curr_char == ",":
                self.minus_space_gulper()
                param = self.parse_attr_param()
                params.append(param)
            elif self.curr_char == ")":
                self.gulp_char()
                break
            else:
                self.raise_syntax_error("parser error, invalid character")

        return tuple(params)

    def parse_attr_param(self):
        value_just_found = False
        while True:
            if value_just_found:
                if self.curr_char == "," or self.curr_char == ")":
                    break
                else:
                    self.raise_syntax_error(
                        "parameters for attributes should be split with a `,` or end with a `)`"
                    )
            else:
                if self.curr_char in NUMBER_VALID_VALS:
                    val = self.parse_number()
                elif self.curr_char == "[":
                    val = self.parse_list()
                else:
                    self.raise_syntax_error(
                        f"invalid value for parameter to start with `{self.curr_char}`"
                    )
                break

            self.gulp_char()
        return val

    def parse_list(self):
        self.check_starting_character("[", "list")
        # remove the first `[`
        self.gulp_char()

        vals = []
        element_just_found = False
        while True:
            if element_just_found:
                if self.curr_char == ",":
                    self.minus_space_gulper()
                    element_just_found = False
                elif self.curr_char == "]":
                    self.gulp_char()
                    break
                else:
                    self.raise_syntax_error(
                        "elements in list should be seperated by a comma"
                    )

            if self.curr_char == '"' or self.curr_char == "'":
                val = self.parse_string()
                vals.append(val)
                element_just_found = True

            elif self.curr_char in NUMBER_VALID_VALS:
                val = self.parse_number()
                vals.append(val)
                element_just_found = True
            else:
                self.raise_syntax_error("invalid character")
        return vals

    def parse_variable_or_number(self):
        var_name = ""
        while True:
            if self.curr_char is None:
                break

            if self.curr_char in string.ascii_letters + string.digits + "_-":
                var_name += self.curr_char
            else:
                break
            self.gulp_char()

        try:
            var = float(var_name)
        except ValueError:
            var = var_name
        return var

    def parse_variable(self):
        var = self.parse_variable_or_number()
        if type(var) == str:
            return var
        else:
            self.raise_syntax_error("value should be a variable and not a number")

    def parse_number(self):
        var = self.parse_variable_or_number()
        if type(var) == float:
            return var
        else:
            self.raise_syntax_error("value should be a number and not a varible")

    def parse_string(self):
        start_char = self.curr_char

        self.check_starting_character(["'", '"'], "string")
        # remove the first `"` or `'`
        self.gulp_char()

        val = ""

        while True:
            if self.curr_char == start_char:
                self.gulp_char()
                break
            elif self.curr_char == "\\":
                self.gulp_char()
                if self.curr_char in ["'", '"', "\\"]:
                    val += self.curr_char
                else:
                    self.raise_syntax_error(f"invalid character : \\{self.curr_char}")
            elif self.curr_char is None:
                self.raise_syntax_error("unterminated string")
            else:
                val += self.curr_char

            self.gulp_char()
        return val

    def check_starting_character(self, chars_to_check, item_type):
        if not isinstance(chars_to_check, list):
            chars_to_check = [chars_to_check]

        if not self.curr_char in chars_to_check:
            self.raise_internal_parser_error(
                "the starting character should be  in {chars_to_check} for a(n) {item_type}"
            )

    def raise_syntax_error(self, error_details):
        raise errors.FlaskValueCheckerSyntaxError(
            textwrap.dedent(
                f"""\
        {error_details}

        error parsing line
        error character position : {self.curr_pos}

        Error in line :
        {self.raw_line}
        {" "*self.curr_pos + "^"}

        at character : `{self.curr_char}`
        """
            )
        )

    def raise_internal_parser_error(self, error_details):
        raise errors.FlaskValueCheckerSyntaxError(
            textwrap.dedent(
                f"""\
        {error_details}

        Internal Parser Error
        (this is NOT the fault of the programmer USING the library,
         only the programmer who WROTE the library)
        error character position : {self.curr_pos}

        Error in line :
        {self.raw_line}
        {" "*self.curr_pos + "^"}

        at character : `{self.curr_char}`
        """
            )
        )

    def __repr__(self):
        if self.is_empty_line:
            return "<{self.__class__.__name__} empty line>"
        elif self.is_comment_line:
            return "<{self.__class__.__name__} comment line>"
        attrs_text = ""

        for attr in self.attrs:
            attr_name, params = attr
            if params:
                attrs_text += f"[{attr_name} params: {params}] "
            else:
                attrs_text += f"[{attr_name}] "

        return f"<{self.__class__.__name__} {self.field_name} ({attrs_text})>"
