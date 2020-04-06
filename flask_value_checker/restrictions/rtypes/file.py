from ..generic_restriction import GenericRestriction
from flask import request


class FileRestriction(GenericRestriction):
    type_keyword = "file"
    attributes = {
        "optional": {},
        "number": {"parameters": [{"type": int}]},
    }

    def __init_restriction__(self):
        self.optional = False

    def compile_restriction(self, name: str, vals: list):
        if name == "optional":
            self.optional = True

    def check_for(self, _):
        if not self.optional:
            if not self.parameter in request.files:
                return False, f"file '{self.parameter}' is missing !"

        return True, None
