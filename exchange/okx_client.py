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
                'defaultType': 'spot',  # Hoặc 'future' nếu bạn dùng hợp đồng
                'demoTrading': use_demo,
            },
        })

        if use_demo:
            self.exchange.set_sandbox_mode(True)

        self.exchange.load_markets()
    
    def get_price(self, symbol):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker['bid'], ticker['ask']

    def get_balance(self):
        return self.exchange.fetch_balance()

    def create_market_buy(self, symbol, amount):
        try:
            # Đặt lệnh mua
            order = self.exchange.create_market_buy_order(symbol, amount)
            print("[OKXClient] Đã đặt lệnh BUY:", order)

            # Nếu trả về giá khớp là float, trả thẳng giá trị đó
            if isinstance(order, float):
                return order  # Trả về giá trị float trực tiếp

            # Nếu trả về kiểu dictionary, tiếp tục kiểm tra giá trung bình
            retries = 0
            while order['average'] is None and retries < 5:  # Thử lại 5 lần
                print("[OKXClient] Lệnh chưa có giá khớp, đang chờ...")
                time.sleep(2)  # Chờ 2 giây
                order = self.exchange.fetch_order(order['id'], symbol)  # Lấy lại thông tin lệnh
                retries += 1

            if order['average'] is None:
                print("[OKXClient] Không có giá khớp, huỷ lệnh...")
                return None

            return order['average']  # Trả về giá trung bình khớp
        except Exception as e:
            print("[OKXClient] Lỗi khi mua:", e)
            return None

    def create_market_sell(self, symbol, amount):
        return self.exchange.create_market_order(symbol=symbol, side='sell', amount=amount)

    def place_order(self, symbol, side, amount, price):
        # Market order thì bỏ price và đổi type thành 'market'
        order = self.exchange.create_limit_order(
            symbol=symbol,
            side=side,  # 'buy' hoặc 'sell'
            amount=amount,
            price=price
        )
        return order
