__all__ = [
    "safe_input",
    "ustr",
]

try:
    safe_input = raw_input
except NameError:
    safe_input = input


try:
    ustr = unicode
except NameError:
    ustr = str
