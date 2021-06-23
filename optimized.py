# livrable = liste d'actions à acheter du type [{'name': 'action1', 'quantity': x},...]

# constraints :   1. buy only 1 action and only once
#                 2. cannot buy a part of action but only a plain number
#                 3.maximum money to spend = 500 euros
#                 4. Read a file containing shares information                          --------  OK
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
        share['Gain'] = int(round(share['Profit']*share['Price']/100.,3)*100)
    return list_of_shares


def dynamic_gain(capital_to_use, shares_list):
    """ dynamic function """
    matrix = [[0 for x in range(capital_to_use + 1)] for x in range(len(shares_list) + 1)]
    for indice in range(1, len(shares_list) + 1):
        for capital in range(capital_to_use + 1):
            if shares_list[indice-1]['Price'] <= capital:
                matrix[indice][capital] = max(matrix[indice-1][capital], shares_list[indice-1]['Gain'] +
                                              matrix[indice-1][capital - shares_list[indice-1]['Price']])
            else:
                matrix[indice][capital] = matrix[indice-1][capital]

    # find the shares used to get the best solution
    capital = capital_to_use
    length = len(shares_list)
    best_shares = []
    while capital >0 and length > 0:
        share = shares_list[length-1]
        if matrix[length][capital] == matrix[length-1][capital-share['Price']] + share['Gain']:
            best_shares.append(share)
            capital -= share['Price']
        length -= 1

    return matrix, best_shares


def main():
    """ main function """
    start = t.time()
    shares_list = read_csv_file(csv_filename)
    shares_list = create_gain_by_share(shares_list)
    matrix, best_shares = dynamic_gain(capital_to_invest, shares_list)
    end = t.time()
    print('temps d exécution du programme = {} secondes'.format(round(end-start, 4)))
    gain_total_euros = round(matrix[-1][-1]/100., 2)
    print('gain total = {} euros soit {}% du capital initial'.format(gain_total_euros, round(gain_total_euros*100./capital_to_invest,2)))
    print('--------  Meilleures actions  --------------------\n', best_shares)
    print("nombre d'actions achetées = ", len(best_shares))

if __name__ == "__main__":
    # print(timeit.timeit("main()", number = 5))
    main()
