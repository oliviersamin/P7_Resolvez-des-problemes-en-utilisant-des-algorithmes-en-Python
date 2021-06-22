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
import time as t
from itertools import permutations as perm


csv_filename = 'data_bruteforce.csv'
capital_to_invest = 500


def read_csv_file(csv_file: str) -> list:
    """ read the csv file and load the list following the format:
        [{'name': 'action1', 'price': 100, 'profit': 10}, ...]"""
    shares_list = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = []
        for index, row in enumerate(reader):
            if index == 0:
                headers = row
            else:
                shares_list.append({headers[0]: row[0], headers[1]: int(row[1]), headers[2]: int(row[2])})
    return shares_list


def sort_shares_list_by_price(share: dict) -> int:
    """ used by transform_list_to_deque() to sort a list of dictionary by 'Profit' key """
    return share['Price']


def sort_shares_list_by_gain(share: dict) -> int:
    """ used by transform_list_to_deque() to sort a list of dictionary by 'Profit' key """
    return share['Gain']


def sorted_list_result(list_shares: list) -> list:
    """  """
    list_shares.sort(key=sort_shares_list_by_gain, reverse=True)
    # print('list_shares = ', list_shares)
    return list_shares


def sorted_list(list_shares: list) -> list:
    """  """
    list_shares.sort(key=sort_shares_list_by_price, reverse=True)
    # print('list_shares = ', list_shares)
    return list_shares


def creation_list_shares_with_price_constraint(best_permutation: list, permutation,
                                               capital_to_use: int) -> list:
    """ select the shares to use in the permutation that respect the total price capital """

    capital_left = capital_to_use
    list_shares = []
    # print('permutation = ', permutation)
    for share in permutation:
        # print(share)
        if capital_left - share['Price'] >= 0:
            list_shares.append(share)
            capital_left -= share['Price']
        # else:
            # print('trop cher')
    # print('list_shares = ',list_shares)
    # print('idem = ', list_shares==permutation)
    best_permutation = get_best_permutation(list_shares, best_permutation)
    return best_permutation


def get_best_permutation(permutation: list, best_permutation: list) -> list:
    """ calculate the profit of a permutation and compare it to the best_permutation
        if better, it become the best permutation, otherwise it is thrown in the trash
        best_permutation = [{'Name': 'Action1', 'Price': 20, 'Profit': 5},..., gains]"""
    gains = 0.
    for share in permutation:
        gains += share['Price']*(share['Profit']/100.)
    gains = round(gains, 2)
    # print(gains)
    try:
        if gains > best_permutation[-1]:
            for share in permutation:
                best_permutation.append(share)
            # print(best_permutation)
            best_permutation.append(gains)
            # print(best_permutation)
            return best_permutation
        else:
            return best_permutation
    except IndexError:
        list_to_return = permutation
        list_to_return.append(gains)
        return(list_to_return)


def operation_to_share_into_processors(permutation, best_permutation, capital):
    """ this is the part of the algorithm that needs to be share for multiprocessing """
    best_permutation = creation_list_shares_with_price_constraint(best_permutation, permutation, capital)
    return best_permutation


def choose_number_of_shares_to_treat(number: int, shares: list, best_permutation: list, capital: int) -> object:
    start = t.localtime()
    test_shares = []
    for index, share in enumerate(shares):
        if index < number:
            test_shares.append(share)
    generator = perm(test_shares)
    # pool = multiprocessing.Pool()
    # operation_to_share_into_processors(generator, best_permutation, capital)
    # temp = partial(operation_to_share_into_processors, "best_permutation", "capital")
    # best_permutation = pool.imap(temp, generator, chunksize=500000)
    # pool.close()
    # pool.join()
    for permutation in generator:
        best_permutation = creation_list_shares_with_price_constraint(best_permutation, permutation, capital)
    best_permutation[-1] = round(best_permutation[-1]/capital*100.,2)
    end = t.localtime()
    duration_hour = end.tm_hour - start.tm_hour
    duration_min = end.tm_min - start.tm_min
    duration_sec = end.tm_sec - start.tm_sec
    print("duree de l'analyse: {} h {} min et {} sec".format(duration_hour, duration_min, duration_sec))
    # print('meilleure permutation = ', best_permutation[:-1])
    print('profit = {}%'.format(best_permutation[-1]))
    return best_permutation


def function_o_2n(capital_max, shares, shares_kept=[]):
    """ use a recursive function to go faster """
    if shares:
        gain1, list_share1, capital = function_o_2n(capital_max, shares[1:], shares_kept)
        share = shares[0]
        if share['Price'] <= capital_max:
            gain2, list_share2, capital = function_o_2n(capital_max - share['Price'], shares[1:], shares_kept +
                                                             [share])
            if gain1 < gain2:
                return gain2, list_share2, capital
        return gain1, list_share1, capital
    else:
        return sum([i['Gain'] for i in shares_kept]), shares_kept, capital_max


def create_gain_by_share(list_of_shares: list) -> list:
    """ get a list of shares and calculate from its 'profit' its 'gain' in euros """
    for share in list_of_shares:
        share['Gain'] = round(share['Profit']*share['Price']/100.,3)
    return list_of_shares


def main():
    """ main function """
    # print('calcul for {} shares'.format(number))
    shares_list = read_csv_file(csv_filename)
    shares_list = create_gain_by_share(shares_list)
    shares = sorted_list(shares_list)
    # print(shares)
    max_gain, list_shares, capital_restant = function_o_2n(capital_to_invest, shares)
    list_shares = sorted_list_result(list_shares)
    # best_permutation = choose_number_of_shares_to_treat(number, shares, best_permutation, capital)
    print('liste d actions: {}\ncapital restant = {} euros'.format(list_shares, len(list_shares), capital_restant))
    print('gain en euros: {} soit {}%'.format(round(max_gain,2), round(max_gain/capital_to_invest*100.,2)))
    print(sorted_list_result(shares))



if __name__ == "__main__":
    # print(timeit.timeit("main()", number = 5))
    main()