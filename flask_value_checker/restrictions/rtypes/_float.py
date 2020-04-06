from ..generic_restriction import GenericRestriction


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

        limits_text = (
            f"{Fore.RED}limits({Style.RESET_ALL}"
            + f"{Fore.GREEN}min :{Fore.RED} {self.min}, {Fore.GREEN}max :{Fore.RED} {self.max}){Style.RESET_ALL}"
        )

        # colored start "<", name and end ">"
        start_part = Fore.CYAN + "<" + padded_name + Style.RESET_ALL
        end_part = Fore.CYAN + ">" + Style.RESET_ALL

        return f"{start_part} {colored_param} {optional_text} {limits_text}{end_part}"
