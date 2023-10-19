import time
import requests
import hmac
import hashlib
import json
import uuid

bas = ('''
██████╗ ██╗   ██╗██████╗ ██╗████████╗     █████╗ ██████╗ ██╗    ███████╗ ██████╗ ███████╗████████╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██║╚══██╔══╝    ██╔══██╗██╔══██╗██║    ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝
██████╔╝ ╚████╔╝ ██████╔╝██║   ██║       ███████║██████╔╝██║    ███████╗██║   ██║█████╗     ██║   
██╔══██╗  ╚██╔╝  ██╔══██╗██║   ██║       ██╔══██║██╔═══╝ ██║    ╚════██║██║   ██║██╔══╝     ██║   
██████╔╝   ██║   ██████╔╝██║   ██║       ██║  ██║██║     ██║    ███████║╚██████╔╝██║        ██║   
╚═════╝    ╚═╝   ╚═════╝ ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝ ╚═════╝ ╚═╝        ╚═╝   
''')
spot = ('''
███████╗██████╗  ██████╗ ████████╗
██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
███████╗██████╔╝██║   ██║   ██║   
╚════██║██╔═══╝ ██║   ██║   ██║   
███████║██║     ╚██████╔╝   ██║   
╚══════╝╚═╝      ╚═════╝    ╚═╝   
''')
futures = ('''
███████╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗███████╗
██╔════╝██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔════╝
█████╗  ██║   ██║   ██║   ██║   ██║██████╔╝█████╗  ███████╗
██╔══╝  ██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  ╚════██║
██║     ╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗███████║
╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
''')
price_name = ('''
██████╗ ██████╗ ██╗ ██████╗███████╗
██╔══██╗██╔══██╗██║██╔════╝██╔════╝
██████╔╝██████╔╝██║██║     █████╗  
██╔═══╝ ██╔══██╗██║██║     ██╔══╝  
██║     ██║  ██║██║╚██████╗███████╗
╚═╝     ╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝
''')

secret_key = None
api_key = None

with open('api_keys.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    if line.startswith('api_key='):
        api_key = line.split('=')[1].strip()
    elif line.startswith('secret_key='):
        secret_key = line.split('=')[1].strip()  #Достается апи из тхт

# -----------------------------------------------------------------------------------------------------------------------------        
     
def hashing(query_string):   #какая то хуйня???
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def futures_market_open_order(symbol, side, orderType, qty, category='linear', takeProfit="", stopLoss=""):      #Фьючерсы маркет открыть ордер
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "qty": "{qty}", "category": "{category}", "takeProfit": "{takeProfit}", "stopLoss": "{stopLoss}"' + '}' 
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)

# -----------------------------------------------------------------------------------------------------------------------------

def futures_limit_open_order(symbol, side, orderType, qty, price, category='linear', takeProfit="", stopLoss=""):      #Фьючерсы лимитка открыть ордер
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "price": "{price}", "qty": "{qty}", "category": "{category}, "takeProfit": "{takeProfit}", "stopLoss": "{stopLoss}""' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)
    
# -----------------------------------------------------------------------------------------------------------------------------  

def futures_cancel_order(symbol, category='linear'):      #Фьючерсы маркет закрыть ордер
    url = 'https://api.bybit.com/v5/order/cancel-all'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)    

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)
# -----------------------------------------------------------------------------------------------------------------------------  

def futures_leverage_order(symbol, Leverage='1', category='linear'):      #Фьючерсы плечо
    url = 'https://api.bybit.com/v5/position/set-leverage'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "buyLeverage": "{Leverage}", "sellLeverage": "{Leverage}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)    

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)
  
# -----------------------------------------------------------------------------------------------------------------------------  

def spot_market_open_order(symbol, side, orderType, qty, category='spot'):        #спот маркет купить/продать
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "qty": "{qty}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)  

# -----------------------------------------------------------------------------------------------------------------------------  

def spot_limit_open_order(symbol, side, orderType, qty, price, category='spot'):      #спот лимитка купить/продать
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "price": "{price}", "qty": "{qty}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)

# -----------------------------------------------------------------------------------------------------------------------------  

def get_price(symbol):                      #узнать цену
    url = f'https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}USDT'
    response = requests.get(url=url)
    data = response.json()
    usd_index_price = data["result"]["list"][0]["usdIndexPrice"]
    print(f"Цена {symbol} = {usd_index_price}$")

# -----------------------------------------------------------------------------------------------------------------------------  

def get_balance(accountType):
    if accountType == "FUND":
        get_balance_fund()
        return
    else:
        endpoint = "https://api.bybit.com/v5/account/wallet-balance"
        url = endpoint
        curr_time = str(int(time.time()*1000))
        payload = f'accountType={accountType}'
        sign = hashing(str(curr_time) + api_key + '5000' + payload)

        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-SIGN": sign,
            "X-BAPI-TIMESTAMP": curr_time,
            "X-BAPI-RECV-WINDOW": "5000",
        }
        response = requests.request("GET", url=(url + "?" + payload), headers=headers)
        data = json.loads(response.text)
        if data.get("retMsg") == "OK":

            total_equity = data["result"]["list"][0]["totalEquity"] # тотал балик
            print(f"Общий баланс: {total_equity} \n")

            coins = data["result"]["list"][0]["coin"]

            if accountType != 'CONTRACT':
                coins = sorted(coins, key=lambda coin: float(coin["usdValue"]), reverse=True)

            # Выводим отсортированные монеты
            for coin in coins:
                if coin["usdValue"] != "":
                    usd_value = float(coin["usdValue"])
                    if usd_value >= 0.03:
                        coin_name = coin["coin"]
                        wallet_balance = coin["walletBalance"]
                        print(f"Монета: {coin_name}, Wallet Balance: {wallet_balance}, USD Value: {round(usd_value, 2)}$")
        else: 
            print("Ошибка, Такого кошелька не существует!")

 # -----------------------------------------------------------------------------------------------------------------------------     

def get_balance_fund():
    endpoint = "https://api.bybit.com/v5/asset/transfer/query-account-coins-balance"
    url = endpoint
    curr_time = str(int(time.time()*1000))
    payload = f'accountType=FUND'
    sign = hashing(str(curr_time) + api_key + '5000' + payload)

    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": sign,
        "X-BAPI-TIMESTAMP": curr_time,
        "X-BAPI-RECV-WINDOW": "5000",
    }
    response = requests.request("GET", url=(url + "?" + payload), headers=headers)
    data = json.loads(str(response.text))

    # Получение информации о балансе для каждой монеты
    for item in data['result']['balance']:
        if  float(item['walletBalance']) != 0:
            coin_name = item['coin']
            wallet_balance = item['walletBalance']
            print(f"Монета: {coin_name}, Баланс кошелька: {wallet_balance}")   

 # -----------------------------------------------------------------------------------------------------------------------------  

def get_list_order(symbol):
    endpoint = "https://api.bybit.com/v5/position/list"
    url = endpoint
    curr_time = str(int(time.time()*1000))
    data = f'category=linear&symbol={symbol}USDT'
    sign = hashing(str(curr_time) + api_key + '5000' + data)

    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": sign,
        "X-BAPI-TIMESTAMP": curr_time,
        "X-BAPI-RECV-WINDOW": "5000",
    }
    response = requests.request("GET", url=(url + "?" + data), headers=headers)
    parsed_data = json.loads(str(response.text))

    list_item = parsed_data['result']['list'][0]
    leverage = list_item['leverage']
    avg_price = list_item['avgPrice']
    liq_price = list_item['liqPrice']
    take_profit = list_item['takeProfit']
    side = list_item['side']
    stop_loss = list_item['stopLoss']
    size = list_item['size']
    Pnl = list_item['unrealisedPnl']

    side = "Long" if side == "Buy" else "Short"
    print(f"Токен: {symbol}")
    print(f"Размер позиции: {size}$")
    print(f"Цена Входа: {avg_price}$")
    print(f"Сторона:", *{side})
    print(f"Плечо: {leverage}x")
    print(f"Take Profit: {take_profit}")
    print(f"Stop Loss: {stop_loss}")
    print(f"Цена Ликвидации: {liq_price}$")
    print(f"PnL: {Pnl}$")

    match input("\n 1. Закрыть позицию \n 2. Обновить информацию \n 3. Выйти\n"):
        case "1":
            side_inverse = "Sell" if side == "Long" else "Buy"
            futures_market_open_order(symbol=f'{symbol}USDT', side=f'{side_inverse}', orderType='Market', qty=f"{size}")    
        case "2":
            get_list_order(symbol)
        case _:
            start()

# -----------------------------------------------------------------------------------------------------------------------------

def Transfer(transferId, coin, amount, fromAccountType, toAccountType):      # Перевод баланса
    url = 'https://api.bybit.com/v5/asset/transfer/inter-transfer'
    current_time = int(time.time() * 1000)
    data = '{' + f'"transferId": "{transferId}", "coin": "{coin}", "amount": "{amount}", "fromAccountType": "{fromAccountType}", "toAccountType": "{toAccountType}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)

# -----------------------------------------------------------------------------------------------------------------------------  

def start():
    print(bas)
    print(" 1. Спот\n 2. Фьючерсы\n 3. Узнать цены\n 4. Баланс аккаунта\n 5. Информация о позициях\n 6. Переводы между счетами\n 7. Выйти\n")
    match input("Ваш выбор? "):
        case '1':
            print(spot)
            choose = input("\nКакой вариант торговли? \n 1. Рыночный \n 2. Лимитный \n 3. Назад \n")
            if choose == "1":                
                symbol = input("каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                side = 'Buy' if input(" 1. Купить\n 2. Продать\n ") == "1" else 'Sell'
                qty  = input("На какую сумму купить(USDT)/продать(TOKEN)? ")
                spot_market_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Market', qty=f"{qty}")
            elif choose == "2":
                symbol = input("каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                side = 'Buy' if input(" 1. Купить\n 2. Продать\n ") == "1" else 'Sell'
                price = float(input("Цена лимитной покупки/продажи: "))
                qty  = input("На какую сумму купить(USDT)/продать(TOKEN)? ")
                spot_limit_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Limit', qty=f'{qty}', price=f'{price}')             
            else:
                start()
        case '2':
            print(futures)
            choose = input("\nКакой вариант торговли? \n 1. Рыночный \n 2. Лимитный \n 3. Назад \n")
            if choose == "1":                
                symbol = input("Каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                Leverage = input("Установите Плечо: ")
                futures_leverage_order(symbol=f'{symbol}USDT', Leverage=f'{Leverage}')
                side = 'Buy' if input(" 1. Лонг\n 2. Шорт\n ") == "1" else 'Sell'
                qty  = input("сумма входа: ")
                TPSL = input("Использовать ли TPSL? \n 1. Да \n 2. Нет \n")
                if TPSL == "1":
                    TP = input("Введите Take Profit: ")    
                    SL = input("Введите Stop Loss: ")   
                    futures_market_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Market', qty=f"{qty}", takeProfit=f"{TP}", stopLoss=f"{SL}")
                else:
                    futures_market_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Market', qty=f"{qty}")
            elif choose == "2":
                symbol = input("Каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                Leverage = input("Установите Плечо: ")
                futures_leverage_order(symbol=f'{symbol}USDT', Leverage=f'{Leverage}')
                side = 'Buy' if input(" 1. Лонг\n 2. Шорт\n ") == "1" else 'Sell'
                price = float(input("Цена лимитной покупки/продажи: "))
                qty  = input("Сумма входа:  ")
                TPSL = input("Использовать ли TPSL? \n 1. Да \n 2. Нет \n")
                if TPSL == "1":
                    TP = input("Введите Take Profit: ")    
                    SL = input("Введите Stop Loss: ")   
                    futures_limit_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Market', qty=f"{qty}", price=f'{price}', takeProfit=f"{TP}", stopLoss=f"{SL}")
                else:
                    futures_limit_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Limit', qty=f'{qty}', price=f'{price}')
            else:
                start()
        case '3':
            print(price_name)
            while True:
                print("(Чтобы выйти введите 0)\n")
                symbol = input(" Введите токен: ").upper()
                if symbol == "0":
                    start()
                    return
                get_price(symbol=f'{symbol}')
        case "4":
            choose = input("\nКакой аккаунт \n 1. ЕТА \n 2. СПОТ \n 3. ДЕРИВАТИВЫ \n 4. ФИНАНСИРОВАНИЕ \n")
            if choose == "1":
                get_balance(accountType='UNIFIED')   
            elif choose == "2":
                get_balance(accountType='SPOT')
            elif choose == "3":
                get_balance(accountType='CONTRACT')
            elif choose == "4":
                get_balance(accountType='FUND')
            else:
                start()   
        case "5":
            symbol = input("Какой токен позиции? ( например BTC, ETH, LTC и тд ) ").upper()
            get_list_order(symbol=f'{symbol}') 
        case "6":
            transfer_dict = {
            '1': 'UNIFIED',
            '2': 'SPOT',
            '3': 'CONTRACT',
            '4': 'FUND'
                            }
            transferId = uuid.uuid4()
            TransferFrom = input("\nОткуда перевести: \n 1. ЕТА \n 2. СПОТ \n 3. ДЕРИВАТИВЫ \n 4. ФИНАНСИРОВАНИЕ \n 5. Выйти\n")
            if TransferFrom in transfer_dict:
                TransferFrom = transfer_dict[TransferFrom]
                get_balance(accountType=TransferFrom)
            else:
                start()
            TransferTo = input("\nКуда перевести: \n 1. ЕТА \n 2. СПОТ \n 3. ДЕРИВАТИВЫ \n 4. ФИНАНСИРОВАНИЕ \n 5. Выйти\n")
            if TransferTo in transfer_dict:
                TransferTo = transfer_dict[TransferTo]
                get_balance(accountType=TransferTo)              
            else:
                start()
            coin = input("Какой токен перевести? ").upper()
            amount = input("Сколько перевести? ")
            
            Transfer(transferId=f'{transferId}', coin=f'{coin}', amount=f'{amount}', fromAccountType=f'{TransferFrom}', toAccountType=f'{TransferTo}')
            time.sleep(3)
            start()
        case "7":
            return
        case _:
            start()     


if __name__ == '__main__':
    start()
