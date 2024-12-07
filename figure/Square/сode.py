_a = 15  # скрытая переменная


def square_perimeter(side=None):
    if side is None:  # если side не передан
        side = _a
    return 4 * side


def square_area(side=None):
    if side is None:  # если side не передан, используем
        side = _a
    return side ** 2