from web3 import Web3
import decimal
import random
import time
from tqdm import tqdm

RPC = "https://eth-goerli.public.blastapi.io"
web3 = Web3(Web3.HTTPProvider(RPC))

def bridge(wallet, proc_gETH_min, proc_gETH_max):
    bridge_abi ='[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EthWithdrawalFinalized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"txId","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"txHash","type":"bytes32"},{"indexed":false,"internalType":"uint64","name":"expirationTimestamp","type":"uint64"},{"components":[{"internalType":"uint256","name":"txType","type":"uint256"},{"internalType":"uint256","name":"from","type":"uint256"},{"internalType":"uint256","name":"to","type":"uint256"},{"internalType":"uint256","name":"gasLimit","type":"uint256"},{"internalType":"uint256","name":"gasPerPubdataByteLimit","type":"uint256"},{"internalType":"uint256","name":"maxFeePerGas","type":"uint256"},{"internalType":"uint256","name":"maxPriorityFeePerGas","type":"uint256"},{"internalType":"uint256","name":"paymaster","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256[4]","name":"reserved","type":"uint256[4]"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256[]","name":"factoryDeps","type":"uint256[]"},{"internalType":"bytes","name":"paymasterInput","type":"bytes"},{"internalType":"bytes","name":"reservedDynamic","type":"bytes"}],"indexed":false,"internalType":"struct IMailbox.L2CanonicalTransaction","name":"transaction","type":"tuple"},{"indexed":false,"internalType":"bytes[]","name":"factoryDeps","type":"bytes[]"}],"name":"NewPriorityRequest","type":"event"},{"inputs":[{"internalType":"uint256","name":"_l2BlockNumber","type":"uint256"},{"internalType":"uint256","name":"_l2MessageIndex","type":"uint256"},{"internalType":"uint16","name":"_l2TxNumberInBlock","type":"uint16"},{"internalType":"bytes","name":"_message","type":"bytes"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"}],"name":"finalizeEthWithdrawal","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"uint256","name":"_l2GasLimit","type":"uint256"},{"internalType":"uint256","name":"_l2GasPerPubdataByteLimit","type":"uint256"}],"name":"l2TransactionBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_l2TxHash","type":"bytes32"},{"internalType":"uint256","name":"_l2BlockNumber","type":"uint256"},{"internalType":"uint256","name":"_l2MessageIndex","type":"uint256"},{"internalType":"uint16","name":"_l2TxNumberInBlock","type":"uint16"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"},{"internalType":"enum TxStatus","name":"_status","type":"uint8"}],"name":"proveL1ToL2TransactionStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_blockNumber","type":"uint256"},{"internalType":"uint256","name":"_index","type":"uint256"},{"components":[{"internalType":"uint8","name":"l2ShardId","type":"uint8"},{"internalType":"bool","name":"isService","type":"bool"},{"internalType":"uint16","name":"txNumberInBlock","type":"uint16"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"bytes32","name":"value","type":"bytes32"}],"internalType":"struct L2Log","name":"_log","type":"tuple"},{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"}],"name":"proveL2LogInclusion","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_blockNumber","type":"uint256"},{"internalType":"uint256","name":"_index","type":"uint256"},{"components":[{"internalType":"uint16","name":"txNumberInBlock","type":"uint16"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct L2Message","name":"_message","type":"tuple"},{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"}],"name":"proveL2MessageInclusion","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_contractL2","type":"address"},{"internalType":"uint256","name":"_l2Value","type":"uint256"},{"internalType":"bytes","name":"_calldata","type":"bytes"},{"internalType":"uint256","name":"_l2GasLimit","type":"uint256"},{"internalType":"uint256","name":"_l2GasPerPubdataByteLimit","type":"uint256"},{"internalType":"bytes[]","name":"_factoryDeps","type":"bytes[]"},{"internalType":"address","name":"_refundRecipient","type":"address"}],"name":"requestL2Transaction","outputs":[{"internalType":"bytes32","name":"canonicalTxHash","type":"bytes32"}],"stateMutability":"payable","type":"function"}]'
    zksynkeraBridge = web3.to_checksum_address('0x1908e2bf4a88f91e4ef0dc72f02b8ea36bea2319') # contract Holograph
    bridge = web3.eth.contract(address=zksynkeraBridge, abi=bridge_abi)

    key = wallet
    account = web3.eth.account.from_key(key).address
    nonce = web3.eth.get_transaction_count(account)
    gas_price = web3.eth.gas_price
    proc_gETH = round(random.uniform(proc_gETH_min, proc_gETH_max), 3)
    balance_gas = web3.eth.get_balance(account)
    balance_gas_2dec = balance_gas / (10**18)
    value_2dec = round(balance_gas_2dec * (proc_gETH / 100),2)
    _value = int(value_2dec * (10 ** 18))
    _contractL2 = account
    _l2Value = _value
    data_k = ''
    _calldata = bytes(data_k, 'ascii')
    gasLimit = web3.eth.estimate_gas(
            {'to': Web3.to_checksum_address(account), 'from': Web3.to_checksum_address(account),
             'value': web3.to_wei(0.0001, 'ether')}) + random.randint(330000, 420000)

    _l2GasLimit = gasLimit*4
    data_list = []
    _refundRecipient = account
    _gasPricePerPubdata = 800
    tx = bridge.functions.requestL2Transaction(_contractL2, _l2Value, _calldata, _l2GasLimit, _gasPricePerPubdata, data_list, _refundRecipient
            ).build_transaction({
            'value': int(_value*1.25),
            'from': account,
            'gas': gasLimit,
            'gasPrice': int(gas_price*30),  # газ который возвращает  рпс слишком низкий  не принимает стоит транза при мультипликаторе 3 пролетает сразу
            'nonce': web3.eth.get_transaction_count(account),
            })
    signed_tx = web3.eth.account.sign_transaction(tx, key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    account = web3.eth.account.from_key(key).address
    print(f'Transaction hash: https://goerli.etherscan.io/tx/{tx_hash.hex()}')
    print('Waiting for receipt...')
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print('Отправил')





if __name__ == '__main__':
    bridge()
