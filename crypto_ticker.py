from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import os
import random as rd

randchars = ["*", "%", "$", "&", "@", "!", "^", "~", "+", "?", "/", "|", "<", ">"]
# replace by your favorite coins
symbols = ["BTC", "ETH", "BNB", "DOGE", "SOL"]

symbol_s = ""
for symbol in symbols:
    symbol_s = symbol_s + symbol + ","
    if symbols.index(symbol) == len(symbols) - 1: symbol_s = symbol_s[:-1]


url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
parameters = {"symbol": symbol_s, "convert": "USD"}

# Replace API Key
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "REPLACE_WITH_YOUR_OWN_API_KEY",
}

session = Session()
session.headers.update(headers)

# refreshes every 2,5 min
refreshrate = 150
symbol_length = 5
price_length = 9


while True:
    try:
        now = time.time()
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        while time.time() - now < refreshrate:
            for crypto in data["data"]:
                meta = data["data"][crypto][0]
                symbol = meta["symbol"]
                price = meta["quote"]["USD"]["price"]
                price_display = f"{price:.2f}"
                rdchar = randchars[rd.randint(0, 13)]
                if len(symbol) < symbol_length:
                    d = symbol_length - len(symbol)
                    dashes = "-" * d
                if len(price_display) < price_length:
                    delta = price_length - len(price_display)
                    rdchar = rdchar + "-" * delta
                print(f"{symbol}USD{dashes}{rdchar}{price_display}$")
            time.sleep(0.05)
            os.system("cls")

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
