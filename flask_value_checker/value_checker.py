from . import restrictions
from flask import request
import textwrap
import colorama


class ValueChecker:
    def __init__(self, text: str):
        """
        create value checkers from text
        """
        self.checkers = restrictions.make_restrictions(text)

    def check_for(self, multidict):
        """
        checks if there are errors in the request,

        Returns
        -------
        dict or None
            dict or None : dict if there are errors, None if there are no errors
        """
        err_fields = {}
        has_errors = False

        for key, checker in self.checkers.items():
            is_valid, message = checker.check_for(multidict)

            if not is_valid:
                err_fields[key] = message
                has_errors = True

        if has_errors:
            return err_fields
        else:
            return None

    def check(self):
        """
        check if it the parameter has been written correctly or not
        """
        if request.method in ["POST", "PUT"]:
            return self.check_for(request.form)
        else:
            return self.check_for(request.args)

    def __repr__(self):
        checkers_text = ""
        for i, (checker_param, checker) in enumerate(self.checkers.items()):
            if not i == 0:
                checkers_text += "\n"
                checkers_text += "            "
            checkers_text += repr(checker)

        Fore = colorama.Fore
        Back = colorama.Back
        Style = colorama.Style

        return textwrap.dedent(
            f"""\
        {Fore.GREEN}<{self.__class__.__name__}{Style.RESET_ALL}
          {Fore.YELLOW}<checkers>{Style.RESET_ALL}
            {checkers_text}
          {Fore.YELLOW}</checkers>{Style.RESET_ALL}
        {Fore.GREEN}>{Style.RESET_ALL}
        """
        )
