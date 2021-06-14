# livrable = liste d'actions à acheter du type [{'name': 'action1', 'quantity': x},...]

# constraints :   1. buy only 1 action and only once
#                 2. cannot buy a part of action but only a plain number
#                 3.maximum money to spend = 500 euros
#                 4. Read a file containing shares information                          --------  OK
#                 5. MUST TRY ALL THE POSSIBLE COMBINATIONS AND SELECT THE BEST ONE
#                 6. Display only the best result

# CALCUL DU PROFIT FINAL = moyenne pondérée = 20% * (x euros/500 euros) + 18% * (y euros/500 euros)...
# MAXIMISER LE PROFIT = avoir le max d'argent en poche soit (argent final - 500)/500

import csv
from collections import deque
import math


csv_filename = 'data_bruteforce.csv'
shares_list = []
results = []
capital = 500


def read_csv_file(csv_file: str) -> None:
    """ read the csv file and load the list following the format:
        [{'name': 'action1', 'price': 100, 'profit': 10}, ...]"""
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = []
        for index, row in enumerate(reader):
            if index == 0:
                headers = row
            else:
                shares_list.append({headers[0]: row[0], headers[1]: int(row[1]), headers[2]: int(row[2])})


def sort_shares_list_by_profit(share: dict) -> int:
    """ used by transform_list_to_deque() to sort a list of dictionary by 'Profit' key """
    return share['Profit']


def transform_list_to_deque(list_shares: list) -> deque:
    """  """
    list_shares.sort(key=sort_shares_list_by_profit, reverse=True)
    # print('list_shares = ', list_shares)
    return deque(list_shares)


def generate_rotations_over_the_deque(deque_to_use: deque):
    """ main function to generate all the rotations needed to get all the possible combinations"""
    count_of_iterations = 0
    list_first_iteration = basic_rotations_over_the_deque(deque_to_use)
    count_of_iterations += 1
    level = 1
    list_for_while_loop = list_first_iteration.copy()
    while level < len(list_first_iteration) - 1:
        list_for_while_loop = loop_over_all_rotations_for_one_level(list_for_while_loop, level)
        level += 1
        print('{}  sur {}'.format(level, len(list_first_iteration) - 1))
    return list_for_while_loop


def loop_over_all_rotations_for_one_level(list_to_use: list, level) -> list:
    """ loop for one level of rotations """
    loop_list = []
    for index, elem in enumerate(list_to_use):
        # print('index = ', index+1)
        temp_list = basic_rotation_over_deque_less_i_elements(elem, level)
        for el in temp_list:
            loop_list.append(el)
        # check_correct_rotations(loop_list[-1])
        # print('len(loop_list) = ', len(loop_list))
    return loop_list


def basic_rotation_over_deque_less_i_elements(deque_to_use: deque, nb_elements) -> list:
    """ generate a deque where there are rotations over all its element but the nb_elements first ones
        example:    input = ([1,2,3,4], nb_elements = 1)
                    output = [[1,2,3,4],[1,4,2,3],[1,3,4,2]]

        example 2:  input = ([1,2,3,4], nb_elements = 2)
                    output = [[1,2,3,4],[1,2,4,3]]
    """

    loop_list = []
    deque_loop = deque_to_use.copy()
    shares = []
    number = 0
    while number < nb_elements:
        number += 1
        shares.append(deque_loop.popleft())
    deque_loop = basic_rotations_over_the_deque(deque_loop)
    for elem in deque_loop:
        loop_list.append(deque(shares))
        for share in elem:
            loop_list[-1].append(share)
    return loop_list


def basic_rotations_over_the_deque(deque_to_use: deque) -> list:
    """ first function to launch when starting algo (generate a list of deque)"""
    number_of_rotations = len(deque_to_use)
    output_list = []
    count = 0
    while count < number_of_rotations:
        list_shares = deque()
        for share in deque_to_use:
            list_shares.append(share)
        output_list.append(list_shares)
        deque_to_use.rotate(1)
        count += 1
    return output_list


def calculate_best_rotation_for_profit(result: list) -> list:
    capital_to_use = 500
    best_profit = 0
    best_rotation = []
    for index, rotation in enumerate(result):
        profit = 0.
        for share in rotation:
            profit += share['Profit']
        if not best_rotation:
            best_profit = profit/len(rotation)
            best_rotation = rotation
        else:
            if profit/len(rotation) > best_profit:
                best_profit = profit/len(rotation)
                best_rotation = rotation
    print('best profit = {} %'.format(round(best_profit, 2)))
    print('capital restant = A CALCULER!!!' )
    print(best_rotation)
    # return best_rotation


def main():
    number = 9
    read_csv_file(csv_filename)
    shares = transform_list_to_deque(shares_list)
    test_shares = []
    for index, share in enumerate(shares):
        if index < number:
            test_shares.append(share)
    test_shares = deque(test_shares)
    final_list = generate_rotations_over_the_deque(test_shares)
    print(len(final_list), math.factorial(number))
    calculate_best_rotation_for_profit(final_list)


if __name__ == "__main__":
    main()
