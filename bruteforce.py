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
    deque_first_iteration = basic_rotations_over_the_deque(deque_to_use)
    count_of_iterations += 1
    check_correct_rotations(deque_first_iteration)
    final_deque = loop_over_all_rotations_for_one_level(deque_first_iteration)
    # print(final_deque)
    return final_deque


def loop_over_all_rotations_for_one_level(deque_to_use: deque) -> list:
    """ loop ok for one level of rotations (if len(deque to use) = n, the rotations will be made
     only for n-1 and not until 2"""
    loop_list = []
    for index, elem in enumerate(deque_to_use):
        print('index = ', index+1)
        temp_list, end_of_loops = basic_rotation_over_deque_less_first_element(elem)
        for el in temp_list:
            loop_list.append(el)
        check_correct_rotations(loop_list[-1])
        print('len(loop_list) = ', len(loop_list), loop_list)
    return loop_list


def basic_rotation_over_deque_less_first_element(deque_to_use: deque) -> list:
    """ generate a deque where there are rotations over all its element but the first one
     example: input = ([1,2,3,4])
            output = ([1,2,3,4],[1,4,2,3],[1,3,4,2])"""
    loop_list = []
    deque_loop = deque_to_use.copy()
    first_share = deque_loop.popleft()
    end_of_loops = (len(deque_loop) == 2)
    print('basic_rotation_over_deque_less_first_element, len(deque_loop) = {}, {}'.format(len(deque_loop), end_of_loops))
    deque_loop = basic_rotations_over_the_deque(deque_loop)
    for elem in deque_loop:
        loop_list.append(elem)
    return loop_list, end_of_loops


def check_correct_rotations(data_to_check):
    """ verify that the rotations made create the right amount of combinations """
    print("combinations created = ", len(data_to_check))


def basic_rotations_over_the_deque(deque_to_use: deque) -> deque:
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
    return deque(output_list)


def calculate_best_rotation_for_profit(result: list) -> list:
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
    # print(best_rotation)
    return best_rotation


def main():
    read_csv_file(csv_filename)
    shares = transform_list_to_deque(shares_list)
    test_shares = []
    for index, share in enumerate(shares):
        if index < 4:
            test_shares.append(share)
    test_shares = deque(test_shares)
    final_deque = generate_rotations_over_the_deque(test_shares)


if __name__ == "__main__":
    main()
