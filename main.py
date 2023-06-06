import random
import json
from web3 import Web3
import decimal
import time
from tqdm import tqdm
import toArbsingl
import toBasesingl
import toOptimism
import tozkSyncEra


def sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)


def wallet():
    with open('wallets.txt', 'r') as f:
         wallets = [row.strip() for row in f]
         return wallets

RPC = "https://eth-goerli.public.blastapi.io"
web3 = Web3(Web3.HTTPProvider(RPC))

############################################  ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ  #######################################
max_chains = 4 # от 1 до 4 сетей для отправки из списка  text_variants
proc_gETH_min = 4     # от 3 процентов аккаунта слать в другую тестовую сеть
proc_gETH_max = 6      # 5 %  максимальный % gETH для перевода в одну сеть от баланса
sleeptime_min = 40     # минимальная задержа  между транзакциями
sleeptime_max = 60     # максимальная задержа  между транзакциями
wal_sleep_min = 160    # минимальная задержка между кошелька
wal_sleep_max = 180    # максимальная задержка между кошелька
text_variants = ["Arbitrum Testnet", "Optimism Testnet", "zkSync Era Testnet", "Base Testnet"]   # При желании лишнее удалить  "Arbitrum Testnet", "Optimism Testnet", "zkSync Era Testnet", "Base Testnet"

###########################################################################################################

wallets = wallet()
random.shuffle(wallets)
numer = 0

for wallet in wallets:
  try:
    numer = numer + 1
    account_add = web3.eth.account.from_key(wallet).address
    print(numer,'################', account_add, '################')
    k = 0
    i = 1
    rnd_way = []
    r = len(text_variants)


    r = random.randint(1,max_chains)  #кол-во случайных активностей
    acc_balance = web3.eth.get_balance(account_add)

    if acc_balance > 0:
     for i in range(r):
      str_ch = random.choice(text_variants)
      text_variants.remove(str_ch)
      k = i+1
      try:
        if str_ch == 'Arbitrum Testnet':
          print('№ бриджа ',k,' ++++++++++ Запуск ',str_ch,'++++++++++')
          toArbsingl.bridge(wallet, proc_gETH_min, proc_gETH_max)
        elif str_ch == 'Base Testnet':
          print('№ бриджа ',k,' ++++++++++ Запуск ',str_ch,'++++++++++')
          toBasesingl.bridge(wallet, proc_gETH_min, proc_gETH_max)
        elif str_ch == 'Optimism Testnet':
          print('№ бриджа ',k,' ++++++++++ Запуск ',str_ch,'++++++++++')
          toOptimism.bridge(wallet, proc_gETH_min, proc_gETH_max)
        elif str_ch == 'zkSync Era Testnet':
          print('№ бриджа ',k,' ++++++++++ Запуск ',str_ch,'++++++++++')
          tozkSyncEra.bridge(wallet, proc_gETH_min, proc_gETH_max)
      except:
          print('Ошибка в работе с кошельком')
      rnd_way.append(str_ch)
      sleeping(sleeptime_min, sleeptime_max)
    else:
      print('На кошельке нет gETH')
    #print(rnd_way)
    if acc_balance == 0:
      pass
    else:
      sleeping(wal_sleep_min,wal_sleep_max)
  except:
   account_add = web3.eth.account.from_key(wallet).address
   print('Ошибка!', account_add)
