from exchange.okx_client import OKXClient
from config import SYMBOL, TRADE_AMOUNT, TAKE_PROFIT_PERCENT, STOP_LOSS_PERCENT
import time

class TradeManager:
    def __init__(self, client, strategy):
        self.client = client
        self.strategy = strategy

    def run(self):
        while True:
            if self.strategy.should_enter_trade(SYMBOL):
                print("[Trade] Điều kiện phù hợp. Vào lệnh...")

                # Mua vào
                order = self.client.create_market_buy(SYMBOL, TRADE_AMOUNT)

                # Kiểm tra nếu order là float, tức là giá mua trực tiếp được trả về
                if isinstance(order, float):
                    buy_price = order
                    print(f"[Trade] Đã mua tại {buy_price}")

                # Nếu order là kiểu dict, kiểm tra 'average' trong order
                elif isinstance(order, dict) and 'average' in order and order['average'] is not None:
                    buy_price = order['average']
                    print(f"[Trade] Đã mua tại {buy_price}")

                else:
                    print("[Trade] Không có giá khớp. Thử lại...")
                    continue

                tp = buy_price * (1 + TAKE_PROFIT_PERCENT / 100)
                sl = buy_price * (1 - STOP_LOSS_PERCENT / 100)
                print(f"[TP/SL] TP: {tp:.4f} - SL: {sl:.4f}")

                coin = SYMBOL.split('/')[0]  # Ví dụ: EOS từ 'EOS/USDT'

                while True:
                    # Lấy số dư đồng coin (EOS, BTC, v.v...)
                    balance_data = self.client.get_balance()

                    try:
                        balance = balance_data[coin]['free']
                    except KeyError:
                        print(f"[Trade] Không lấy được số dư {coin}. Dữ liệu: {balance_data}")
                        break

                    print(f"[Trade] Số dư hiện tại ({coin}): {balance}")

                    if balance < TRADE_AMOUNT:
                        print(f"[Trade] Không đủ số dư để bán. Số dư hiện tại: {balance}")
                        break

                    bid, _ = self.client.get_price(SYMBOL)
                    print(f"[Monitor] Giá hiện tại: {bid:.4f}")

                    if bid >= tp:
                        print("[TP] Chốt lời...")
                        self.client.create_market_sell(SYMBOL, TRADE_AMOUNT)
                        break
                    elif bid <= sl:
                        print("[SL] Cắt lỗ...")
                        self.client.create_market_sell(SYMBOL, TRADE_AMOUNT)
                        break

                    time.sleep(3)

            else:
                print("[Trade] Spread lớn quá, chờ cơ hội...")

            time.sleep(5)
