import copy

from tables import SimplexTable
from suport import SYSTEM_ACCURACY


class Simplex:
    __s_tables_history__: list[SimplexTable]
    __no_result__ = False

    def __init__(
            self,
            func_coefs: list[float],
            conf_coefs: list[list[float]],
            point_coords: list[float]
    ):
        self.__s_tables_history__ = []
        self.__s_tables_history__.append(
            SimplexTable(
                copy.copy(func_coefs),
                copy.deepcopy(conf_coefs),
                copy.copy(point_coords),
            )
        )

    def __find_resolving_element(self):
        min_delta = 1
        min_ratio = -1
        re_row = -1
        re_col = -1
        table = self.__s_tables_history__[-1]
        for col in range(len(deltas := table.deltas)):
            if deltas[col] < 0 and deltas[col] <= min_delta:
                min_delta = deltas[col]
                negative_counter = 0
                for row in range(len(x_inds := table.b_indexes)):
                    if table.table[row][col] <= 0:
                        negative_counter += 1
                        if negative_counter == len(x_inds):
                            return -1, -1
                    elif (ratio := round(
                            table.point[x_inds[row]] / table.table[row][col], SYSTEM_ACCURACY
                    )) < min_ratio or min_ratio == -1:
                        min_ratio = ratio
                        re_row = row
                        re_col = col
        return re_row, re_col

    def __generate_new_table__(self):
        re_row, re_col = self.__find_resolving_element()
        if re_row == -1:
            return -1
        table = self.__s_tables_history__[-1]
        new_point = [0] * len(table.point)
        new_table = [[0] * len(table.table[0]) for _ in table.table]
        new_x_inds = [0] * len(table.b_indexes)
        for row in range(len(x_inds := table.b_indexes)):
            if row != re_row:
                new_x_inds[row] = x_inds[row]
                new_point[x_inds[row]] = round(
                    table.point[x_inds[row]] - table.point[x_inds[re_row]]
                    * table.table[row][re_col] / table.table[re_row][re_col],
                    SYSTEM_ACCURACY
                )
                for col in range(len(table.point)):
                    new_table[row][col] = round(
                        table.table[row][col] - table.table[re_row][col]
                        * table.table[row][re_col] / table.table[re_row][re_col],
                        SYSTEM_ACCURACY
                    )
            else:
                new_x_inds[row] = re_col
                new_point[re_col] = round(
                    table.point[x_inds[re_row]] / table.table[re_row][re_col], SYSTEM_ACCURACY
                )
                for col in range(len(table.point)):
                    new_table[row][col] = round(
                        table.table[re_row][col] / table.table[re_row][re_col], SYSTEM_ACCURACY
                    )
        self.__s_tables_history__.append(
            SimplexTable(table.coefficients, new_table, new_point, new_x_inds)
        )

    def get_result(self) -> (list[float], float):
        if self.__no_result__:
            return None
        return copy.copy(self.__s_tables_history__[-1].point), \
               self.__s_tables_history__[-1].values[-1]

    def get_tables_history(self) -> list[SimplexTable]:
        return list(map(copy.copy, self.__s_tables_history__))

    def calculate_simplex(self) -> int:
        self.__no_result__ = False
        self.__s_tables_history__ = [self.__s_tables_history__[0]]
        while not self.__s_tables_history__[-1].is_positive_delta():
            if self.__generate_new_table__() == -1:
                self.__no_result__ = True
                break
