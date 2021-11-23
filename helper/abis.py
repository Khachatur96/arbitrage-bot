from web3 import Web3


def result_by_get_expected_rate(address_1, address_2, amount, contract):
    price_result = '{:.4f}'.format(contract.functions.getExpectedRate(
        Web3.toChecksumAddress(address_1),
        Web3.toChecksumAddress(address_2),
        int(amount),
    ).call()[0] / 1000000000000000000)

    return price_result


def result_by_get_amounts_out(address_1, address_2, amount, decimal, contract):
    price_result = '{:.4f}'.format(contract.functions.getAmountsOut(
        int(amount),
        [Web3.toChecksumAddress(address_1),
         Web3.toChecksumAddress(address_2)]).call()[1] / decimal)

    return price_result


def result_by_view_split_exact_out(address_1, address_2, amount, contract):
    price_result = contract.functions.viewSplitExactOut(
        Web3.toChecksumAddress(address_1),
        Web3.toChecksumAddress(address_2),
        amount,
        2
    ).call()[1] / 1000000000000000000

    return price_result


def result_by_get_expected_return(address_1, address_2, amount, decimal, contract):

    price_result = '{:.4f}'.format(contract.functions.getExpectedReturn(
        Web3.toChecksumAddress(address_1),
        Web3.toChecksumAddress(address_2),
        amount, 2, 2).call()[0] / decimal)
    return price_result


def result_by_get_estimated_swap_amount(address_1, address_2, amount, contract, decimal):
    price_result = '{:.4f}'.format(contract.functions.get_estimated_swap_amount(
        Web3.toChecksumAddress(address_1),
        Web3.toChecksumAddress(address_2),
        int(amount),
    ).call() / decimal)

    return price_result
