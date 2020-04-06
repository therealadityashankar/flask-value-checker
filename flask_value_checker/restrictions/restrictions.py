"""
all the restrictions in flask-value-checker

make sure to create a new restriction be subclassing GenericRestriction,
make sure the subclass has a 'prefix' property

then make sure to add it in the restrictions array in the make_restriction
function
"""
import textwrap
import colorama
from .rtypes._float import FloatRestriction
from .rtypes._int import IntRestriction
from .rtypes.string import StringRestriction
from .rtypes.file import FileRestriction

from .generic_restriction import GenericRestriction


def get_restriction_classes():
    return [StringRestriction, FloatRestriction, IntRestriction, FileRestriction]
