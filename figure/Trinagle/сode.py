import math
_a = 7  # длины сторон
_b = 2
_c = 8


def triangle_perimeter(a=None, b=None, c=None):
    if a is None:  # если аргументы не переданы, значения по умолчанию
        a = _a
    if b is None:
        b = _b
    if c is None:
        c = _c
    return a + b + c


def triangle_area(a=None, b=None, c=None):
    if a is None:
        a = _a
    if b is None:
        b = _b
    if c is None:
        c = _c
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))