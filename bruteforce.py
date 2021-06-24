# livrable = liste d'actions à acheter du type [{'name': 'action1', 'quantity': x},...]

# constraints :   1. buy only 1 action and only once
#                 2. cannot buy a part of action but only a plain number
#                 3.maximum money to spend = 500 euros
#                 4. Read a file containing shares information                          --------  OK
#                 5. MUST TRY ALL THE POSSIBLE COMBINATIONS AND SELECT THE BEST ONE
#                 6. Display only the best result

import csv
import time as t


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


def create_gain_by_share(list_of_shares: list) -> list:
    """ get a list of shares and calculate from its 'profit' its 'gain' in euros """
    for share in list_of_shares:
        share['Gain'] = round(share['profit']*share['price']/100.,3)
    return list_of_shares


def brute_force_gain(capital_max, shares, shares_kept=[]):
    """ use a recursive function to go faster """
    if shares:
        gain1, list_share1, capital = brute_force_gain(capital_max, shares[1:], shares_kept)
        share = shares[0]
        if share['price'] <= capital_max:
            gain2, list_share2, capital = brute_force_gain(capital_max - share['price'], shares[1:], shares_kept +
                                                             [share])
            if gain1 < gain2:
                return gain2, list_share2, capital
        return gain1, list_share1, capital
    else:
        return sum([i['Gain'] for i in shares_kept]), shares_kept, capital_max


def brute_force_pourcentage(capital_max, shares, shares_kept=[]):
    """ use a recursive function to go faster """
    if shares:
        p1, list_share1, capital = brute_force_pourcentage(capital_max, shares[1:], shares_kept)
        share = shares[0]
        if share['price'] <= capital_max:
            p2, list_share2, capital = brute_force_pourcentage(capital_max - share['price'], shares[1:],
                                                                  shares_kept + [share])
            if p1 < p2:
                return p2, list_share2, capital
        return p1, list_share1, capital
    else:
        return sum([i['profit'] for i in shares_kept]), shares_kept, capital_max


def main():
    """ main function """
    # print('calcul for {} shares'.format(number))
    start = t.time()
    shares_list = read_csv_file(csv_filename)
    shares_list = create_gain_by_share(shares_list)
    max_gain, list_shares, capital_restant = brute_force_gain(capital_to_invest, shares_list)
    # total_pourcentage, list_shares2, capital_restant2 = brute_force_pourcentage(capital_to_invest, shares)
    # gain = sum([share['Gain'] for share in list_shares2])
    # list_shares = sorted_list_result(list_shares)
    end = t.time()
    print('------ GAIN -------')
    print('liste d actions: {}\ncapital restant = {} euros'.format(list_shares, capital_restant))
    print("nombre d'actions achetées = ", len(list_shares))
    print('gain en euros: {} soit {}%'.format(round(max_gain,2), round(max_gain/capital_to_invest*100.,2)))
    print('temps d exécution du programme = {} secondes'.format(round(end-start,2)))

    for share in list_shares:
        print(share['name'])

    # print('------ POURCENTAGE -------')
    # print('liste d actions: {}\ncapital restant = {} euros'.format(list_shares2, len(list_shares2), capital_restant2))
    # print('gain en euros: {} soit {}%'.format(round(gain,2), round(gain/capital_to_invest*100.,2)))
    # print(total_pourcentage)
    # print('temps d exécution du programme = {} secondes'.format(round(end-start,2)))


if __name__ == "__main__":
    # print(timeit.timeit("main()", number = 5))
    main()
