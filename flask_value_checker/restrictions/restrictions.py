"""
all the restrictions in flask-value-checker

make sure to create a new restriction be subclassing GenericRestriction,
make sure the subclass has a 'prefix' property

then make sure to add it in the restrictions array in the make_restriction
function
"""
import textwrap
import orchid66
import colorama

from .generic_restriction import GenericRestriction


def get_restriction_classes():
    return [StringRestriction, FloatRestriction, IntRestriction]


class StringRestriction(GenericRestriction):
    type_keyword = "str"
    attributes = {
        "optional": {},
        "lenlim": {"parameters": [{"type": int}, {"type": int}]},
        "allow_only": {"parameters": "infinite"},
    }

    def __init_restriction__(self):
        self.optional = False
        self.minlength = 0
        self.maxlength = float("inf")

    def compile_restriction(self, name: str, vals: list):
        """see GenericRestriction.compile_restriction(...) docs"""
        if name == "optional":
            self.optional = True

        elif name == "lenlim":
            self.minlength = vals[0]
            self.maxlength = vals[1]

    def check_for(self, checking_part):
        """see GenericRestriction.check_for docs"""
        value = checking_part.get(self.parameter, None)

        if value is None:
            if self.optional:
                return True, None

            return False, "value is required"

        if not (len(value) >= self.minlength and len(value) <= self.maxlength):
            return (
                False,
                f"string length must be between {self.minlength} and {self.maxlength}",
            )

        return True, None

    def __repr__(self):
        Fore = colorama.Fore
        Back = colorama.Back
        Style = colorama.Style
        optional_text = "optional" if self.optional else ""
        optional_text = Fore.YELLOW + optional_text + Style.RESET_ALL
        colored_param = Fore.GREEN + self.parameter + Style.RESET_ALL

        # name text
        class_names_lens = [len(c.__name__) for c in get_restriction_classes()]
        max_class_name_size = max(class_names_lens)
        padded_name = self.__class__.__name__.ljust(max_class_name_size)
        colored_name = Fore.CYAN + padded_name + Style.RESET_ALL

        return f"<{colored_name} {colored_param} {optional_text} length(min : {self.minlength}, max : {self.maxlength})>"


class FloatRestriction(GenericRestriction):
    type_keyword = "float"
    attributes = {
        "optional": {},
        "lim": {"parameters": [{"type": float}, {"type": float}]},
    }

    def __init_restriction__(self):
        self.optional = False
        self.min = -float("inf")
        self.max = float("inf")

    def compile_restriction(self, name: str, vals: list):
        """
        compile a restriction based on its name and value
        """
        if name == "optional":
            self.optional = True
        elif name == "lim":
            self.min, self.max = vals

    def check_for(self, checking_part):
        """see GenericRestriction.check_for docs"""
        value = checking_part.get(self.parameter, None)

        if value is None:
            if self.optional:
                return True, None
            else:
                return False, "value is required"

        try:
            value = float(value)
        except ValueError:
            return False, f"value {value} cannot be parsed into an float"

        if not (value >= self.min and value <= self.max):
            return False, f"value must be between {self.min} and {self.max}"

        return True, None

    def __repr__(self):
        Fore = colorama.Fore
        Back = colorama.Back
        Style = colorama.Style
        optional_text = "optional" if self.optional else ""
        optional_text = Fore.YELLOW + optional_text + Style.RESET_ALL
        colored_param = Fore.GREEN + self.parameter + Style.RESET_ALL

        # name text
        class_names_lens = [len(c.__name__) for c in get_restriction_classes()]
        max_class_name_size = max(class_names_lens)
        padded_name = self.__class__.__name__.ljust(max_class_name_size)
        colored_name = Fore.CYAN + padded_name + Style.RESET_ALL

        return f"<{colored_name} {colored_param} {optional_text} limits(min : {self.min}, max : {self.max}>"


class IntRestriction(FloatRestriction):
    type_keyword = "int"

    def check_for(self, checking_part):
        """see GenericRestriction.check_for docs"""
        value = checking_part.get(self.parameter, None)

        if value is None:
            if self.optional:
                return True, None
            else:
                return False, "value is required"

        try:
            value = int(value)
        except ValueError:
            return False, f"value {value} cannot be parsed into an int"

        if not (value >= self.min and value <= self.max):
            return False, f"value must be between {self.min} and {self.max}"

        return True, None
