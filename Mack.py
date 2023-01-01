import math
import numpy as np


pointed_elements = []

# matrix = [[9, 20, 60, 15, 21],
#           [38, 71, 69, 49, 60],
#           [28, 13, 80, 28, 34],
#           [58, 34, 13, 37, 25],
#           [30, 3, 53, 20, 21]]

matrix = [[36, 28, 36, 48, 26],
          [32, 24, 35, 42, 28],
          [38, 40, 40, 54, 34],
          [62, 54, 56, 50, 58],
          [30, 41, 35, 58, 38]]

# matrix = [[39, 44, 28, 24, 36],
#           [42, 46, 38, 34, 32],
#           [55, 51, 58, 49, 53],
#           [40, 50, 36, 28, 30],
#           [36, 48, 32, 35, 31]]


def condition(min_i_rows, matrix):
    if len(set(min_i_rows)) == len(matrix[0]):
        return True
    else:
        return False


def preparation(matrix, maximize):
    matr = np.array(matrix.copy(), dtype=float)
    lst_ = []
    if maximize:
        lst_ = np.amax(matr, axis=0)
    else:
        lst_ = np.amin(matr, axis=0)
    for i in range(len(matr[0])):
        for j in range(len(matr)):
            matr[j][i] = abs(matr[j][i] - lst_[i])
    min_in_rows = np.amin(matr, axis=1)
    for i in range(len(matr)):
        matr[i] -= min_in_rows[i]
    return matr


def step_1(matrix):
    print("Step 1")
    min_i_rows = [None] * len(matrix)
    for i in range(len(matrix)):
        min_i_rows[i] = np.argmin(matrix[i])

    if condition(min_i_rows, matrix):
        print_ans(min_i_rows)
        return min_i_rows
    print("Minimal values are in columns: ", min_i_rows)
    step_2(matrix, min_i_rows, [None] * len(matrix[0]))


def step_2(matrix, min_i_rows, pointed_columns):
    print("Step 2")
    arr = np.array(min_i_rows)
    for i in set(min_i_rows):
        if (arr == i).sum() > 1:
            pointed_columns[i] = "+"
    print("Pointed columns are: ", pointed_columns)
    step_3(matrix, min_i_rows, pointed_columns)


def find_ind(lst_, value, pointed_columns):
    for i in range(len(lst_)):
        if lst_[i] == value and pointed_columns[i] != '+':
            return i


def step_3(matrix, min_i_rows, pointed_columns):
    print("Step 3")
    matrix_copy = np.copy(matrix)
    lst_min = []

    for i in range(len(pointed_columns)):
        if pointed_columns[i] == "+":
            for j in range(len(matrix)):
                matrix_copy[j][i] = math.inf
    print(matrix_copy)
    for i in range(len(min_i_rows)):
        lst_min.append([[None, None], None])
        if pointed_columns[min_i_rows[i]] == '+':
            lst_min[i][1] = min(list(matrix_copy[i]))
            j = find_ind(matrix[i], lst_min[i][1], pointed_columns)
            lst_min[i][0][0], lst_min[i][0][1] = i, j
    print("Minimum in each column: ", lst_min)
    min_sub = [math.inf, math.inf], math.inf
    for i in range(len(lst_min)):
        if lst_min[i][1] is not None:
            if lst_min[i][1] - matrix[i][min_i_rows[i]] < min_sub[1]:
                min_sub = lst_min[i][0], lst_min[i][1] - matrix[i][min_i_rows[i]]
    print("Minimal substraction is on indexes: ", min_sub)
    step_4(matrix, min_sub, pointed_columns, min_i_rows)


def step_4(matrix, min_sub, pointed_columns, min_i_rows):
    print("Step 4")
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if pointed_columns[j] == "+":
                matrix[i][j] += min_sub[1]
    print("New matrix: ")
    print(matrix)
    step_5(matrix, min_sub, min_i_rows, pointed_columns)


def step_5(matrix, min_sub, min_i_rows, pointed_columns):
    print("Step 5")
    pointed_elements.append(min_sub[0])
    print("Pointed elements are: ", pointed_elements)
    step_6(matrix, min_sub, min_i_rows, pointed_columns)


def step_6(matrix, min_sub, min_i_rows, pointed_columns):
    print("Step 6")
    if min_sub[0][1] in min_i_rows:
        pointed_columns[min_sub[0][1]] = "+"
        print("Pointed columns are: ", pointed_columns)
        step_3(matrix, min_i_rows, pointed_columns)
    else:
        print("Pointed columns are: ", pointed_columns)
        step_7_8(matrix, min_sub, min_i_rows, pointed_columns)


def step_7_8(matrix, min_sub, min_i_rows, pointed_columns):
    print("Step 7-8")
    pointed_elements.pop()
    temp_column = min_i_rows[min_sub[0][0]]
    min_i_rows[min_sub[0][0]] = min_sub[0][1]
    print("Pointed elements are: ", pointed_elements)
    print("Minimal values are in columns: ", min_i_rows)
    step_9(matrix, min_sub, min_i_rows, pointed_columns, temp_column)


def step_9(matrix, min_sub, min_i_rows, pointed_columns, temp_column):
    print("Step 9")
    if temp_column in min_i_rows:
        step_10(matrix, min_i_rows)
    else:
        for i in range(len(pointed_elements)):
            if pointed_elements[i][1] == temp_column:
                min_i_rows[pointed_elements[i][0]] = temp_column
        print("Minimal values are in columns: ", min_i_rows)
        step_7_8(matrix, min_sub, min_i_rows, pointed_columns)


def step_10(matrix, min_i_rows):
    print("Step 10")
    if not condition(min_i_rows, matrix):
        pointed_columns = [None] * len(matrix[0])
        print("Pointed columns are: ", pointed_columns)
        step_2(matrix, min_i_rows, pointed_columns)
    else:
        print_ans(min_i_rows)


def print_ans(min_i_rows):
    sum = 0
    print("Underscored final optimal values in matrix: ")
    for i in range(len(min_i_rows)):
        sum += matrix[i][min_i_rows[i]]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if j == min_i_rows[i]:
                print(f"({matrix[i][j]})", end=' ')
            else:
                print(matrix[i][j], end=' ')
        print()
    print("Sum is: ", sum)


maximize = True  # set false to minimize

matrix_copy = preparation(matrix, maximize)
print(matrix_copy)
step_1(matrix_copy)


