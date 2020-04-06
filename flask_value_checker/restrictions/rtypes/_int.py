from ._float import FloatRestriction


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
