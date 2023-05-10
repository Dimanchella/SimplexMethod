from functools import reduce

SYSTEM_ACCURACY = 6
OUTPUT_ACCURACY = 2


def calculate_basis_indexes(point: list[float]) -> list[int]:
    b_indexes = []
    for i in range(len(point)):
        if point[i] != 0:
            b_indexes.append(i)
    return b_indexes


def add_fictitious_x(
        function: list[float],
        confines: list[list[float]],
        conf_values: list[float]
) -> tuple[list[float], list[list[float]], list[float]]:
    new_function = [0] * len(function) + [-1] * len(confines)
    new_confines = list(
        map(
            lambda conf, m: conf + [0] * m + [1] + [0] * (len(confines) - 1 - m),
            confines,
            range(len(confines))
        )
    )
    new_point = [0] * len(function) + conf_values
    return new_function, new_confines, new_point


def validate_values(
        function: list[float],
        confines: list[list[float]],
        conf_values: list[float],
        point: list[float]
) -> bool:
    error_codes = []
    if len(conf_values) != len(confines):
        error_codes.append(-5)
    if not __is_eq_len_func_conf__(function, confines):
        error_codes.append(-3)
    if point:
        b_indexes = calculate_basis_indexes(point)
        if len(b_indexes) != len(confines):
            error_codes.append(-1)
        if len(function) != len(point):
            error_codes.append(-2)
        if -3 not in error_codes and not __have_zero_basis__(b_indexes, confines):
            error_codes.append(-4)
    return error_codes


def __is_eq_len_func_conf__(function: list[float], confines: list[list[float]]):
    return reduce(
        lambda b1, b2: b1 and b2,
        map(lambda conf: len(conf) == len(function), confines)
    )


def __have_zero_basis__(b_indexes: list[int], confines: list[list[float]]):
    return not reduce(
        lambda b1, b2: b1 or b2,
        map(lambda bi: reduce(
            lambda b1, b2: b1 and b2,
            map(lambda conf: conf[bi] == 0, confines)
        ), b_indexes)
    )
