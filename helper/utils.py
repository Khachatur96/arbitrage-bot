from web3 import Web3
from datetime import datetime, timezone, timedelta

from extensions import web3
from config import config
from .abis import *
import time

# connects to smart_contract and gets pair price for given swap
# def get_coins_pair_price(swap_address, swap_abi, from_coin, to_coin, proc_num, return_dict):
def get_coins_pair_price(pair):
    """
    :param tuple with pairs info params:
    :return:
        pair_price
    """
    result = {}
    # from_price = 0
    for swap in config.SWAPS:
        contract = web3.eth.contract(address=swap['address'], abi=swap['abi'])
        if swap['name'] == 'OneSplit':
            try:
                response_result = result_by_get_expected_return(address_1=pair[0], address_2=pair[1],
                                                            amount=int(pair[3]), decimal=pair[-1], contract=contract)
            except Exception as e:
                pass
        elif swap['name'] == 'Balancer':
            try:
                response_result = result_by_view_split_exact_out(address_1=pair[0], address_2=pair[1],
                                                             amount=int(pair[3]), contract=contract)
            except Exception as e:
                pass

        elif swap['name'] == 'Kyber':
            try:
                response_result = result_by_get_expected_rate(address_1=pair[0], address_2=pair[1],
                                                              amount=int(pair[3]), contract=contract)
            except Exception as e:
                pass
        elif swap['name'] == 'Curve':
            try:
                response_result = result_by_get_estimated_swap_amount(address_1=pair[0], address_2=pair[1],
                                                                  amount=int(pair[3]), decimal=pair[-1],
                                                                  contract=contract)
            except Exception as e:
                pass
        else:
            try:
                response_result = result_by_get_amounts_out(address_1=pair[0], address_2=pair[1],
                                                        amount=int(pair[3]), decimal=pair[-1], contract=contract)
            except Exception as e:
                pass
        result[swap['name']] = float(response_result)

    # result['from_coin'] = from_price
    result['pair'] = pair[-3]

    return result


# connects to smart_contract and gets pair price for given swap
def get_time_now_in_local_timezone(timezone_offset=0.4):
    """

    :param timezone_offset:
    :return: datetime in string representation
    """
    timezone_info = timezone(timedelta(hours=timezone_offset))

    return datetime.now(timezone_info)


async def buy_token(coin,contract, nonce):
    pancakeswap2_txn = contract.functions.swapExactETHForTokens(
        10000, [config.weth, coin],
        config.wallet_address,
        (int(time.time()) + 1000000)
    ).buildTransaction({
        'from': config.wallet_address,
        'value': web3.toWei('0.01', 'ether'),
        'gas': 250000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(web3.toHex(tx_token))

async def approve(token, spender_address, nonce):

    tx = token.functions.approve(spender_address, 10000000000).buildTransaction({
        'from': config.wallet_address,
        'nonce': nonce
    })

    signed_tx = web3.eth.account.signTransaction(tx, config.private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    print(web3.toHex(tx_hash))



async def swap_tokens_for_tokens(contract,coin_1, coin_2, nonce):
    tokens_for_tokens = contract.functions.swapExactTokensForTokens(
        100000000000, 0, [coin_1, coin_2],
        config.wallet_address,
        (int(time.time()) + 100000)
    ).buildTransaction({
        'from': config.wallet_address,
        'value': web3.toWei('0.01', 'ether'),  # This is the Token(BNB) amount you want to Swap from
        'gas': 25000000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(tokens_for_tokens, private_key=config.private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(web3.toHex(tx_token))
