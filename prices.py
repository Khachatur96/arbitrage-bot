import datetime
import itertools

from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Pool

import pandas as pd
import numpy as np

import gspread
from gspread_dataframe import set_with_dataframe

from extensions import client
from config import config

from helper.utils import get_time_now_in_local_timezone
from helper.utils import get_coins_pair_price


# returns price of given pair using binance client
def get_price_by_symbol_pair_symbol(symbol_pair):
    """
    :param symbol_pair:
    :return: pair_price
    """

    price = client.get_symbol_ticker(symbol=symbol_pair)
    return price['price']


# returns prices in matrix
def get_pairs_matrix():
    """
    Using multiprocessing with Pool
    :return: result of pair prices in different swaps
    """

    pair_info = [(pair['coin_1'].address, pair['coin_2'].address, '-'.join((pair['coin_1'].name, pair['coin_2'].name)),
                  pair['coin_1'].decimals, pair['coin_2'].decimals)
                 for pair in config.PAIRS]
    with Pool(processes=20) as pool:
        results = pool.map(get_coins_pair_price, pair_info)

    return results


# collects prices for all given swaps in config using get_coins_pair_price from utils.py
def get_same_pair_price_in_different_swaps():
    """
    :return:
        dictionary_with_key_swapName_value_price
    """

    processes = []
    manager = Manager()
    return_dict = manager.dict()

    for swap in config.SWAPS:
        proc = Process(target=get_coins_pair_price,
                       args=(swap['address'], swap['abi'], config.COINS['WBNB'], config.COINS['BUSD'], swap['name'],
                             return_dict), )
        processes.append(proc)
        proc.start()
    for proc in processes:
        proc.join()

    return return_dict


# gives final result with required |(min, max, pair, average_percent, date_added)| fields
def sort_pair_price_result():
    """
    :return:
        dictionary_with_final_info
    """
    prices_result = np.array(get_pairs_matrix())
    data_collector = []
    # Result = namedtuple('Result', 'swap_pair difference_percent date_added price_difference all_prices coin_pair')
    # accumulate = prices_subtraction_in_matrix()

    for price_list in prices_result:
        only_swaps = dict(list(price_list.items())[:len(config.SWAPS)])

        sorted_prices = {k: v for k, v in sorted(only_swaps.items(), key=lambda item: item[1])}
        data_collector += (
            [
                price_list['pair'],
                '-'.join(swap_pair),
                get_time_now_in_local_timezone(4.0).strftime("%m/%d/%Y, %H:%M:%S"),
                '{:.4f}'.format(sorted_prices[swap_pair[1]] - sorted_prices[swap_pair[0]]),
                *(f'{k}({v})' for k, v in sorted_prices.items()),
            ]
            for swap_pair in itertools.combinations(sorted_prices.keys(), 2))
        # data_collector.append(accumulate)

    collected_data = pd.DataFrame(data_collector,
                                  columns=['coin_pair', 'swap_pair', 'date_added', 'price_defference',
                                           *[f'dex_{i + 1}' for i in range(len(config.SWAPS))]])
    collected_data.to_csv(f"results/result_{config.CHAIN_NAME}.csv")
    # data_collector.append(accumulate)

    return data_collector


# gives matrix of price difference between high and low  |  (calculating by nm.subtract matrices)
def prices_subtraction_in_matrix():
    """
    :return:
        matrix_with_subtracted_values_of_pair_prices
                                                [[ 0.71895375]
                                                 [31.2062972 ]
                                                 [ 0.23650757]]

    """
    prices_result = np.array(get_pairs_matrix())
    prices_result = [dict(list(pair_row.items())[:len(config.SWAPS)]) for pair_row in prices_result]

    will_be_matrix = [{k: v for k, v in sorted(only_swaps.items(), key=lambda item: item[1])}
                      for only_swaps in prices_result]

    price_info_for_matrix = np.matrix([[value for value in row.values() if not isinstance(value, str)]
                                       for row in will_be_matrix])

    separated_matrices = [price_info_for_matrix[:, i] for i in range(len(price_info_for_matrix))]
    subtraction_result = np.subtract(separated_matrices[-1], separated_matrices[0])
    # print(subtraction_result[0:, 0:1])
    # print({k: k for k in numpy.asarray(subtraction_result)})
    return subtraction_result


def result_to_google_sheets():
    google_sheet_id = '1eDB4_C7hNmM-28DZgWxsjzx_qVN_wgeTMenq8VrsR0E'

    service_account_filename = 'test1-316510-624349e4ac61.json'
    prices_result = get_pairs_matrix()
    data_collector = list()

    aa = sort_pair_price_result()
    print(aa)
    for price_list in prices_result:
        only_swaps = dict(tuple(price_list.items())[:-1])
        final_result = {k: v for k, v in sorted(only_swaps.items(), key=lambda item: item[1])}

        data_collector.append(
            (get_time_now_in_local_timezone(4.0).strftime("%m/%d/%Y"),
             tuple(final_result.keys())[0],
             tuple(final_result.keys())[-1],
             price_list['pair'],
             round(100 - (float(final_result[tuple(final_result.keys())[0]]) /
                          float(final_result[tuple(final_result.keys())[-1]])) * 100, 2),
             'xxx'
             )
        )
    curr_df = pd.DataFrame(aa, columns=('coin_pair','swap_pair','date_added','price_defference','dex_1','dex_2','dex_3','dex_4','dex_5','dex_6'))
    # current_dataframe = pd.DataFrame(data_collector,
    #                                  columns=('Date', 'DEX Low', 'DEX High', 'Pair', 'Slippage', 'Gas Price'))

    gc = gspread.service_account(filename=service_account_filename)
    sh = gc.open_by_key(google_sheet_id)
    current_worksheet = sh.worksheet("New Results")

    set_with_dataframe(current_worksheet, curr_df, 1, 1)


if __name__ == '__main__':
    start = datetime.datetime.now()
    sort_pair_price_result()
    print(datetime.datetime.now() - start)
    # result_to_google_sheets()
