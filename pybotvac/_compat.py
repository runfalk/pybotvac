try:
    ustr = unicode
except NameError:
    ustr = str

strtypes = (ustr, bytes)
