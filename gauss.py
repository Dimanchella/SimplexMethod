import copy

from tables import FloatTable
from suport import SYSTEM_ACCURACY


class GaussMethod:
    __tables_history__: list[FloatTable]
    __b_indexes__: list[int]

    def __init__(self, conf_coefs: list[list[float]], b_indexes: list[int]):
        self.__tables_history__ = [FloatTable(copy.deepcopy(conf_coefs))]
        self.__b_indexes__ = copy.copy(b_indexes)

    def __is_independent_basis__(self) -> bool:
        for ri in range(len(table := self.__tables_history__[-1].table)):
            for bi in range(len(b_inds := self.__b_indexes__)):
                if not (ri == bi and table[ri][b_inds[bi]] == 1 or table[ri][b_inds[bi]] == 0):
                    return False
        return True

    def get_result(self) -> FloatTable:
        return copy.deepcopy(self.__tables_history__[-1])

    def get_tables_history(self) -> list[FloatTable]:
        return copy.deepcopy(self.__tables_history__)

    def get_basis_indexes(self) -> list[int]:
        return copy.copy(self.__b_indexes__)

    def calculate_gauss(self):
        self.__tables_history__ = [self.__tables_history__[0]]
        b_inds = self.__b_indexes__
        for i in range(len(self.__tables_history__[-1].table)):
            if self.__is_independent_basis__():
                break
            new_table = copy.deepcopy(self.__tables_history__[-1].table)
            if new_table[i][b_inds[i]] == 0:
                for i_swap in range(i + 1, len(new_table)):
                    if new_table[i_swap][b_inds[i]] != 0:
                        new_table[i], new_table[i_swap] = new_table[i_swap], new_table[i]
                        break
            new_table[i] = list(map(
                lambda el:
                round(el / new_table[i][b_inds[i]], SYSTEM_ACCURACY),
                new_table[i]
            ))
            for j in range(len(new_table)):
                if i != j and new_table[j][b_inds[i]] != 0:
                    new_table[j] = list(map(
                        lambda elj, eli: elj - eli,
                        new_table[j], map(
                            lambda el: el * new_table[j][b_inds[i]],
                            new_table[i]
                        )
                    ))
            self.__tables_history__.append(FloatTable(new_table))
