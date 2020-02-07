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
        for restriction in self.raw_restrictions:
            name, vals = restriction
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
            "{parameter}" should have {param_count} value(s),
            it currently has {len(values)} values

            error in line:
            {self.raw_line}
            """
                )
            )

    def _check_parameter_type(self, para_type, parameter, value):
        if para_type == "int" or para_type == int:
            is_float = isinstance(value, float)
            str_val = str(value)

            intable = False
            is_some_infinity = False

            if is_float:
                is_some_infinity = str_val == "inf" or str_val == "-inf"
                if not is_some_infinity:
                    intable = (value - int(value)) == 0

            if is_float and (intable or is_some_infinity):
                if is_some_infinity:
                    return value
                else:
                    value = int(value)
                    return value
            else:
                raise errors.FlaskValueCheckerValueError(
                    textwrap.dedent(
                        f"""\
                restriction "{parameter}" cannot have the value "{value}",
                as it cannot be compiled into an `int`(or isn't "inf" i.e. infinity)

                error in line: {self.raw_line}
                """
                    )
                )

        elif para_type == "float" or para_type == float:
            if isinstance(value, float):
                return value
            else:
                raise errors.FlaskValueCheckerValueError(
                    textwrap.dedent(
                        f"""\
                restriction "{parameter}" cannot have the value "{value}",
                as it isn't of type `float`

                error in line: {self.raw_line}
                """
                    )
                )

        elif para_type.startswith("list of "):
            list_type_str = para_type[len("list of ") :]
            if not isinstance(value, list):
                raise errors.FlaskValueCheckerValueError(
                    textwrap.dedent(
                        f"""\
                restriction "{parameter}" cannot have the value "{value}",
                as it isn't if type `list`

                error in line: {self.raw_line}
                """
                    )
                )

            if list_type_str == "ints" or list_type_str == "int":
                list_type = int
            elif list_type_str == "float" or list_type_str == "floats":
                list_type = float
            elif list_type_str == "str" or list_type_str == "strs":
                list_type = str

            vals = value
            for val in vals:
                if not isinstance(val, list_type):
                    raise errors.FlaskValueCheckerValueError(
                        textwrap.dedent(
                            f"""\
                    restriction "{parameter}" cannot have the value "{value}",
                    as not everything in the list is of type `{list_type}`

                    error in line: {self.raw_line}
                    """
                        )
                    )
            return vals

        raise errors.FlaskValueCheckerValueError(
            textwrap.dedent(
                f"""\
        Internal flask-value-checker error,

        if you're seeing this,
        this error is not the fault of the person using the library but of the fault
        of the creator of the library

        unknown para_type: {para_type}

        error in line: {self.raw_line}
        """
            )
        )

    def compile_restriction(self, name: str, vals: list):
        """compile a restriction based on its name and value"""
        return NotImplementedError(
            "this function should be overridden by subclassing class"
        )

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
