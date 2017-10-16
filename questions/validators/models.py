import re
from django.core.validators import _lazy_re_compile, RegexValidator
from django.utils.translation import ugettext_lazy as _


def str_list_validator(sep=',', message=None, code='invalid', allow_negative=False):
    """A modified version of the django str_int_validator function for strings."""
    regexp = _lazy_re_compile(r'^[\w ]+(?:%(sep)s[\w ]+)*\Z' % {
        'sep': re.escape(sep),
    })
    return RegexValidator(regexp, message=message, code=code)


validate_comma_separated_string_list = str_list_validator(
    message=_('Enter strings separated by commas. '
              'Only the characters a-z, A-Z, 0-9, underscores, and spaces are supported'),
)
