import copy
from functools import reduce

import suport


class FloatTable:
    table: list[list[float]]

    def __init__(self, list_2d: list[list[float]]):
        self.table = copy.deepcopy(list_2d)

    def __str__(self):
        chars = list(map(lambda row: list(map(
            lambda el: str(round(el, suport.OUTPUT_ACCURACY)), row
        )), self.table))
        max_char_len = max(list(map(
            lambda cs_row: max(list(map(len, cs_row))),
            chars
        )))
        for i in range(len(chars)):
            for j in range(len(chars[0])):
                chars[i][j] = ' ' * (max_char_len - len(chars[i][j])) + chars[i][j]
        return "\n".join(list(map(' '.join, chars)))

    def __copy__(self):
        return FloatTable(copy.deepcopy(self.table))


class SimplexTable(FloatTable):
    coefficients: list[float]
    values: list[float]
    deltas: list[float]
    point: list[float]
    b_indexes: list[int]

    def __init__(
            self,
            coefs: list[float],
            table: list[list[float]],
            point: list[float],
            x_indexes=None
    ):
        super().__init__(table)
        self.coefficients = copy.copy(coefs)
        self.point = copy.copy(point)
        if x_indexes:
            self.b_indexes = copy.copy(x_indexes)
        else:
            self.b_indexes = suport.calculate_basis_indexes(point)
        self.__calculate_values__()
        self.__calculate_deltas__()

    def __str__(self):
        chars = [
            list(map(str, ['B', 'c', '~x'] + list(map(
                lambda c: round(c, suport.OUTPUT_ACCURACY), self.coefficients
            ))))
        ]
        for row in range(len(self.table)):
            chars.append(list(map(str, reversed(
                list(map(lambda t: round(t, suport.OUTPUT_ACCURACY), reversed(self.table[row])))
                + [round(self.point[self.b_indexes[row]], suport.OUTPUT_ACCURACY)]
                + [round(self.coefficients[self.b_indexes[row]], suport.OUTPUT_ACCURACY)]
                + [f"x{self.b_indexes[row] + 1}"]
            ))))
        chars.append(
            list(map(str, ['z', ' '] + list(map(
                lambda v: round(v, suport.OUTPUT_ACCURACY),
                [self.values[-1]] + self.values[0:-1]
            ))))
        )
        chars.append(
            list(map(str, ['d', ' ', ' '] + list(map(
                lambda d: round(d, suport.OUTPUT_ACCURACY), self.deltas
            ))))
        )
        max_char_len = max(list(map(
            lambda cs_row: max(list(map(len, cs_row))),
            chars
        )))
        for i in range(len(chars)):
            for j in range(len(chars[0])):
                chars[i][j] = ' ' * (max_char_len - len(chars[i][j])) + chars[i][j]
        return "\n".join(list(map(' '.join, chars)))

    def __copy__(self):
        return SimplexTable(
            copy.copy(self.coefficients),
            copy.deepcopy(self.table),
            copy.copy(self.point),
            copy.copy(self.b_indexes)
        )

    def __calculate_values__(self):
        self.values = []
        for col in range(len(self.coefficients)):
            value = 0
            for row in range(len(self.b_indexes)):
                value += round(
                    self.coefficients[self.b_indexes[row]] * self.table[row][col],
                    suport.SYSTEM_ACCURACY
                )
            self.values.append(value)
        value = 0
        for row in range(len(self.b_indexes)):
            value += round(
                self.coefficients[self.b_indexes[row]] * self.point[self.b_indexes[row]],
                suport.SYSTEM_ACCURACY
            )
        self.values.append(value)

    def __calculate_deltas__(self):
        self.deltas = list(map(
            lambda v, c: v - c,
            self.values, self.coefficients
        ))

    def is_positive_delta(self):
        return reduce(
            lambda b1, b2: b1 and b2,
            list(map(
                lambda a: a >= 0,
                self.deltas
            ))
        )
