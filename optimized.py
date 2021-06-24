# livrable = liste d'actions à acheter du type [{'name': 'action1', 'quantity': x},...]

# constraints :   1. buy only 1 action and only once
#                 2. cannot buy a part of action but only a plain number
#                 3.maximum money to spend = 500 euros
#                 4. Read a file containing shares information                          --------  OK
#                 6. Display only the best result


import csv
import time as t


csv_basic = 'data_bruteforce.csv'
capital_to_invest = 500
csv_backtest1 = 'bactest_set1_donnees.csv'
csv_backtest2 = 'bactest_set2_donnees.csv'


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
                shares_list.append({headers[0]: row[0], headers[1]: int(float(row[1])*100), headers[2]: int(float(row[2])*100)})
    return shares_list


def filter_shares(list_of_shares: list) -> list:
    """ filter errors that could occur while getting data """
    validated_shares = []
    for share in list_of_shares:
        if share['price'] > 0:
            validated_shares.append(share)
    return validated_shares


def create_gain_by_share(list_of_shares: list) -> list:
    """ get a list of shares and calculate from its 'profit' its 'gain' in euros """
    for share in list_of_shares:
        share['Gain'] = int(round(share['profit']*share['price']/(100.*100), 3))
    return list_of_shares


def dynamic_gain(capital_to_use, shares_list) -> tuple:
    """ dynamic function """
    matrix = [[0 for y in range(capital_to_use + 1)] for x in range(len(shares_list) + 1)]
    for indice in range(1, len(shares_list) + 1):
        for capital in range(capital_to_use + 1):
            if shares_list[indice-1]['price'] <= capital:
                matrix[indice][capital] = max(matrix[indice-1][capital], shares_list[indice-1]['Gain'] +
                                              matrix[indice-1][capital - shares_list[indice-1]['price']])
            else:
                matrix[indice][capital] = matrix[indice-1][capital]

    # find the shares used to get the best solution
    capital = capital_to_use
    length = len(shares_list)
    best_shares = []
    while capital > 0 and length > 0:
        share = shares_list[length-1]
        if matrix[length][capital] == matrix[length-1][capital-share['price']] + share['Gain']:
            best_shares.append(share)
            capital -= share['price']
        length -= 1

    return matrix, best_shares


def final_analysis(csv_file, display) -> None:
    """ analyse the original set of 20 actions asked and print results """
    start = t.time()
    # to avoid issues with prices and capital with non integer values
    capital_max = int(capital_to_invest*100)
    shares_list = read_csv_file(csv_file)
    shares_list = filter_shares(shares_list)
    shares_list = create_gain_by_share(shares_list)
    matrix, best_shares = dynamic_gain(capital_max, shares_list)
    end = t.time()
    duration = round(end-start, 4)
    gain_total_euros = round(matrix[-1][-1]/100., 2)
    percentage = round(gain_total_euros * 100. / capital_to_invest, 2)
    best_shares_display = []
    total_cost = 0.
    for share in best_shares:
        best_shares_display.append(share['name'])
        total_cost += share['price']/100

    if display == 'basic':
        print('----------------------------- JEU DE 20 ACTIONS PROPOSEES  -----------------------------')
    elif display == 'backtest1':
        print('----------------------------- BACKTEST 1  -----------------------------')
    elif display == 'backtest2':
        print('----------------------------- BACKTEST 2  -----------------------------')
    print('temps d exécution du programme = {} secondes'.format(duration))
    print('gain total = {} euros soit {}% du capital initial'.format(gain_total_euros, percentage))
    print("nombre d'actions achetées = ", len(best_shares))
    print("cout total = {} euros".format(total_cost))
    print('Actions choisies:\n', best_shares_display)


def main():
    """ main function """
    # final_analysis(csv_basic, 'basic')
    final_analysis(csv_backtest1, 'backtest1')
    final_analysis(csv_backtest2, 'backtest2')


if __name__ == "__main__":
    # print(timeit.timeit("main()", number = 5))
    main()
