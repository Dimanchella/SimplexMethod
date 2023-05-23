import json
import sys
from functools import reduce

from gauss import GaussMethod
from simplex import Simplex
import suport

ERROR_CODE = -1


def error_check(
        func: list[float], confs: list[list[float]],
        confs_values: list[float], point: list[float]
):
    if len(error_codes := suport.validate_values(func, confs, confs_values, point)) > 0:
        error_str = ""
        if -1 in error_codes:
            error_str += "\nКоличество базисных (ненулевых) переменных в стартовой точке не" \
                         " соответствует количеству уравнений в системе ограничений!"
        if -2 in error_codes:
            error_str += "\nКоличество переменных в стартовой точке не соответствует" \
                         " количеству переменных в исходной функции!"
        if -3 in error_codes:
            error_str += "\nКоличество переменных в одном или нескольких уравнениях в" \
                         " системе ограничений не соответствует количеству переменных в" \
                         " исходной функции!"
        if -4 in error_codes:
            error_str += "\nОдна или несколько базисных (ненулевых) переменных в стартовой" \
                         " точке полностью отсутствует в системе ограничений!"
        if -5 in error_codes:
            error_str += "\nКоличество значений системы ограничений не соответствует" \
                         " количеству уравнений в системе ограничений!"
        raise ValueError(error_str)


def start_pre_simplex(
        func: list[float], confs: list[list[float]], confs_vals: list[float]
) -> list[float]:
    pre_func, pre_confs, pre_point = suport.add_fictitious_x(func, confs, confs_vals)
    pre_simplex = Simplex(pre_func, pre_confs, pre_point)
    pre_simplex.calculate_simplex()
    print("\nPRE-SIMPLEX:\n" + "\n\n".join(list(map(str, pre_simplex.get_tables_history()))))
    found_point = pre_simplex.get_result()[0]
    print(f"\nsx: {list(map(lambda x: round(x, suport.OUTPUT_ACCURACY), found_point))}")
    if reduce(
            lambda b1, b2: b1 and b2,
            map(lambda x: x == 0, found_point[len(function):])
    ):
        return found_point[0:len(function)]
    return None


def start_gauss(confs: list[list[float]], point: list[float]) -> list[list[float]]:
    gauss = GaussMethod(confs, suport.calculate_basis_indexes(point))
    gauss.calculate_gauss()
    print(
        f"\nGAUSS:\nbasis indexes: {list(map(lambda b: b + 1, gauss.get_basis_indexes()))}\n"
        + "\n\n".join(list(map(str, gauss.get_tables_history())))
    )
    return gauss.get_result().table


def start_simplex(
        func: list[float], confs: list[list[float]], point: list[float]
):
    simplex = Simplex(func, confs, point)
    simplex.calculate_simplex()
    print("\nSIMPLEX:\n" + "\n\n".join(list(map(str, simplex.get_tables_history()))))
    return simplex.get_result()


if __name__ == '__main__':
    function: list[float]
    confines: list[list[float]]
    confines_values: list[float]
    start_point: list[float]
    try:
        with open("input6.json", "r") as json_file:
            input_dict = json.load(json_file)
            function = input_dict["F"]
            confines = input_dict["A"]
            confines_values = input_dict["B"]
            start_point = input_dict["X"]
        error_check(function, confines, confines_values, start_point)
    except FileNotFoundError as fnfe:
        print(f"Файл input1.json не найден.\n{fnfe}")
        sys.exit(ERROR_CODE)
    except ValueError as ve:
        print(ve)
        sys.exit(ERROR_CODE)

    if not start_point:
        start_point = start_pre_simplex(function, confines, confines_values)
    if not start_point:
        print("\nНет решений!")
    else:
        result = start_simplex(function, start_gauss(confines, start_point), start_point)
        if result:
            print(f"\n~x: {list(map(lambda x: round(x, suport.OUTPUT_ACCURACY), result[0]))}"
                  f"\nz: {round(result[1], suport.OUTPUT_ACCURACY)}")
        else:
            print("\nНет решений!")
