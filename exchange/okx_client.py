import ccxt
import time


class OKXClient:
    def __init__(self, api_key, secret_key, passphrase, use_demo=False):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

        self.exchange = ccxt.okx({
            'apiKey': self.api_key,
            'secret': self.secret_key,
            'password': self.passphrase,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'demoTrading': use_demo,
            },
        })

        self.exchange.set_sandbox_mode(use_demo)
        self.exchange.load_markets()

        print("Sandbox Mode:", use_demo)
        self.print_initial_balances()

    def print_initial_balances(self):
        try:
            balance = self.exchange.fetch_balance()
            print("USDT available:", balance.get('USDT', {}).get('free', 0.0))
            print("EOS available:", balance.get('EOS', {}).get('free', 0.0))
        except Exception as e:
            print("[OKXClient] Lỗi khi lấy số dư ban đầu:", e)

    def get_available_balance(self, asset='USDT'):
        try:
            balance = self.exchange.fetch_balance()
            return balance.get(asset, {}).get('free', 0.0)
        except Exception as e:
            print(f"[OKXClient] Lỗi khi lấy số dư {asset}:", e)
            return 0.0

    def get_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['bid'], ticker['ask']

    def get_balance(self):
        return self.exchange.fetch_balance()

    def create_market_buy(self, symbol, amount):
        try:
            order = self.exchange.create_market_buy_order(symbol, amount)
            print("[OKXClient] Đã đặt lệnh BUY:", order)

            if isinstance(order, float):
                return order

            retries = 0
            while order.get('average') is None and retries < 5:
                print("[OKXClient] Lệnh chưa có giá khớp, đang chờ...")
                time.sleep(2)
                order = self.exchange.fetch_order(order['id'], symbol)
                retries += 1

            if order.get('average') is None:
                print("[OKXClient] Không có giá khớp, huỷ lệnh...")
                return None

            return order['average']
        except Exception as e:
            print("[OKXClient] Lỗi khi mua:", e)
            return None

    def create_market_sell(self, symbol, amount):
        try:
            order = self.exchange.create_market_order(symbol=symbol, side='sell', amount=amount)
            print("[OKXClient] Đã đặt lệnh SELL:", order)
            return order
        except Exception as e:
            print("[OKXClient] Lỗi khi bán:", e)
            return None

    def place_order(self, symbol, side, amount, price):
        try:
            order = self.exchange.create_limit_order(
                symbol=symbol,
                side=side,
                amount=amount,
                price=price
            )
            return order
        except Exception as e:
            print("[OKXClient] Lỗi khi đặt limit order:", e)
            return None

    def fetch_ohlcv(self, symbol, timeframe='1m', limit=20):
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception as e:
            print(f"[OKXClient] Lỗi khi fetch OHLCV: {e}")
            return []
