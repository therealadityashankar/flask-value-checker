from ..generic_restriction import GenericRestriction


class StringRestriction(GenericRestriction):
    type_keyword = "str"
    attributes = {
        "optional": {},
        "lenlim": {"parameters": [{"type": int}, {"type": int}]},
        "accept": {"parameters": [{"type": "list of strs"}]},
    }

    def __init_restriction__(self):
        self.optional = False
        self.minlength = 0
        self.maxlength = float("inf")
        self.accept = None

    def compile_restriction(self, name: str, vals: list):
        """see GenericRestriction.compile_restriction(...) docs"""
        if name == "optional":
            self.optional = True

        elif name == "lenlim":
            self.minlength = vals[0]
            self.maxlength = vals[1]

        elif name == "accept":
            self.accept = vals[0]

    def check_for(self, checking_part):
        """see GenericRestriction.check_for docs"""
        value = checking_part.get(self.parameter, None)

        if self.accept is not None:
            if value is None:
                if self.optional:
                    return True, None
                elif len(self.accept) == 1:
                    return (
                        False,
                        f"value should be '{self.accept[0]}'",
                    )
                else:
                    return (False, f"value must be one from the list {self.accept}")

            if not (len(value) >= self.minlength and len(value) <= self.maxlength):
                return (
                    False,
                    f"string length must be between {self.minlength} and {self.maxlength}",
                )

            if value in self.accept:
                return True, None
            else:
                if len(self.accept) == 1:
                    if self.optional:
                        return (
                            False,
                            f"value should be '{self.accept[0]}', or the field should not be submitted",
                        )
                    else:
                        return (
                            False,
                            f"value should be '{self.accept[0]}'",
                        )
                else:
                    return (False, f"value must be one from the list {self.accept}")
        else:
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
        optional_text = "optional " if self.optional else ""
        optional_text = Fore.YELLOW + optional_text + Style.RESET_ALL
        colored_param = Fore.GREEN + self.parameter + Style.RESET_ALL

        # name text
        class_names_lens = [len(c.__name__) for c in get_restriction_classes()]
        max_class_name_size = max(class_names_lens)
        padded_name = self.__class__.__name__.ljust(max_class_name_size)

        # colored start "<", name and end ">"
        start_part = Fore.CYAN + "<" + padded_name + Style.RESET_ALL
        end_part = Fore.CYAN + ">" + Style.RESET_ALL

        if self.accept is not None:
            accepts_text = (
                Fore.RED
                + "accepts("
                + Fore.GREEN
                + f"{self.accept}"
                + f"{Fore.RED}){Style.RESET_ALL}"
            )
            return (
                f"{start_part} {colored_param} {optional_text}{accepts_text}{end_part}"
            )

        length_text = f"{Fore.RED}length({Fore.GREEN}min :{Fore.RED} {self.minlength}, {Fore.GREEN}max :{Fore.RED} {self.maxlength}{Fore.RED}){Style.RESET_ALL}"
        return f"{start_part} {colored_param} {optional_text}{length_text}{end_part}"
