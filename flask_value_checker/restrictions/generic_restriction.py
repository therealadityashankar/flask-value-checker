from flask import request

from . import errors
import textwrap


class GenericRestriction:
    """
    GenericRestriction,

    all restrictions must be a subclass of this
    """

    def __init__(self, raw_line: str, parameter: str, raw_restrictions: str):
        self.raw_line = raw_line
        self.parameter = parameter
        self.raw_restrictions = raw_restrictions

        self.__init_restriction__()
        self.compile()

    def compile(self):
        for raw_rest in self.raw_restrictions:
            name, vals = self.get_restriction_from_text(raw_rest)
            name, vals = self.check_and_nicefy_attribute(name, vals)
            self.compile_restriction(name, vals)

    def check_and_nicefy_attribute(self, name, params):
        """
        checks if an attribute has been written properly
        """
        # check if the attribute should exist, i.e.,
        # 'required', 'lenlim' for an 'str' restriction
        # are valid but 'someInvalidAttribute' isn't
        attr_style = self.attributes.get(name, None)
        self._check_attribute_existance(attr_style, name)

        # check if the attribute should have parameters,
        # eg: 'required' should not have parameters,
        # but 'lenlim' should
        param_styles = attr_style.get("parameters", [])
        self._check_parameter_presence(param_styles, name, params)

        to_ret_params = []
        for i, param in enumerate(params):
            param_style = param_styles[i]
            para_type = param_style["type"]
            param = self._check_parameter_type(para_type, name, param)
            to_ret_params.append(param)

        return name, to_ret_params

    def _check_attribute_existance(self, attr_style, name):
        if attr_style is None:
            raise errors.FlaskValueCheckerValueError(
                textwrap.dedent(
                    f"""\
            invalid restriction name `{name}`

            error in line: {self.raw_line}
            """
                )
            )

    def _check_parameter_presence(self, parameter_styles, parameter, values):
        param_count = len(parameter_styles)
        if len(values) != param_count:
            raise errors.FlaskValueCheckerValueError(
                textwrap.dedent(
                    f"""\
            {parameter} should have {param_count} value(s),
            it currently has {len(values)} values

            error in line:
            {self.raw_line}
            """
                )
            )

    def _check_parameter_type(self, para_type, parameter, value):
        if para_type == "int" or para_type == int:
            try:
                if value == "inf" or value == "-inf":
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                raise errors.FlaskValueCheckerValueError(
                    textwrap.dedent(
                        f"""\
                restriction {parameter} cannot have the value {value},
                as it cannot be compiled into an `int`

                error in line: {self.raw_line}
                """
                    )
                )

        elif para_type == "float" or para_type == float:
            try:
                value = float(value)
            except ValueError:
                raise errors.FlaskValueCheckerValueError(
                    textwrap.dedent(
                        f"""\
                restriction {parameter} cannot have the value {value},
                as it cannot be compiled into an `float`

                error in line: {self.raw_line}
                """
                    )
                )

        return value

    def compile_restriction(self, name: str, vals: list):
        """compile a restriction based on its name and value"""
        return NotImplementedError(
            "this function should be overridden by subclassing class"
        )

    def get_restriction_from_text(self, restriction_text: str):
        """
        get the restiction value from the restriction_text,

        Returns
        -------
        restiction_name, value
        restriction_name : str
            name of the restriction
        value : str or None
            value of the restriction, i.e. on the right side of '=',
            None if there is no '=' in the restriction_text

        Examples
        --------
        >>> self.get_restriction_from_text('str')
        str, None

        >>> self.get_restriction_from_text('length_range(0, 3)')
        maxlength, [0, 3]
        """
        if "(" in restriction_text:
            attr, params = restriction_text.split("(", 2)

            if not params[-1] == ")":
                raise errors.FlaskValueCheckerSyntacticError(
                    textwrap.dedent(
                        f"""\
                    attributes with parameters must end with a ')'

                    error in line:
                    {self.raw_line}
                """
                    )
                )

            params = params[:-1]
            params = params.split(",")
            params = [value.strip() for value in params]
            return attr, params
        else:
            attr = restriction_text
            return attr, []

    def check_parameter_as(self, restriction_name, restriction_val, equal_parameter):
        """
        check a parameter as its an `=` parameter or not
        """
        if equal_parameter:
            if restriction_val is None:
                raise errors.FlaskValueCheckerValueError(
                    textwrap.dedent(
                        f"""\
                {restriction_name} should have a value, i.e. a `=` parameter,

                error in line: {self.raw_line}
                """
                    )
                )
        else:
            if restriction_val is not None:
                raise errors.FlaskValueCheckerValueError(
                    textwrap.dedent(
                        f"""\
                {restriction_name} should not have a value, i.e. a `=` parameter,

                error in line: {self.raw_line}
                """
                    )
                )

    def check_for(self, checking_part):
        """
        check if the value is acceptable in request form/query

        Parameters
        ----------
        checking_part
            request.form/request.args/a multidict

        Returns
        -------
        is_valid, message

        is_valid : bool
            is the value acceptable or not ?

        message : str or None
            if not valid, returns why the value is invalid

        Examples
        --------
        >>> from flask import request
        then in a function defination, that is called only in the
        flask request context
        >>> string_restriction.check_for(request.form)
        """
        return NotImplementedError(
            "this function should be overridden by subclassing class"
        )

    def __repr__(self):
        return textwrap.dedent(
            f"""\
        <{self.__class__.__name__}
         raw_code_line : '{self.raw_line}'
         parameter_name : '{self.parameter}'
         raw_restrictions : '{self.raw_restrictions}'
         required : {self.required}
        >"""
        )
