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
                print(f"[TP/SL] TP: {tp:.2f} - SL: {sl:.2f}")

                while True:
                    # Lấy số dư tài khoản (kiểm tra dữ liệu trả về)
                    balance_data = self.client.get_balance()  # Không truyền SYMBOL

                    # Giả sử balance_data chứa thông tin tài khoản và số dư trong 'free' hoặc 'balance'
                    # Cần trích xuất số dư cho SYMBOL cụ thể
                    balance = balance_data.get('free', {}).get(SYMBOL, 0.0)  # Trích xuất số dư cho SYMBOL

                    print(f"[Trade] Số dư hiện tại: {balance}")

                    # Kiểm tra số dư trước khi bán
                    if balance < TRADE_AMOUNT:
                        print(f"[Trade] Không đủ số dư. Số dư hiện tại: {balance}")
                        break  # Dừng giao dịch nếu không đủ số dư

                    bid, _ = self.client.get_price(SYMBOL)
                    print(f"[Monitor] Giá hiện tại: {bid:.2f}")

                    # Kiểm tra và thực hiện chốt lời hoặc cắt lỗ
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

