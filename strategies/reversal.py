from utils.risk_control import is_gap_too_large, should_stop_loss, calculate_tp_sl
from config import SPREAD_THRESHOLD, TRADE_AMOUNT, STOP_LOSS_PERCENT, TAKE_PROFIT_PERCENT

class ReversalStrategy:
    def __init__(self, client, ma_period=20, threshold=0.002, gap_threshold_percent=3.0, max_loss_usdt=5):
        self.client = client
        self.ma_period = ma_period
        self.threshold = threshold  # Mặc định 0.2%
        self.gap_threshold_percent = gap_threshold_percent  # Ngưỡng tụt giá mạnh (3%)
        self.max_loss_usdt = max_loss_usdt  # Tối đa lỗ cho phép
        self.last_price = None  # Giá lần trước để so sánh

    def should_enter_trade(self, symbol):
        ohlcv = self.client.fetch_ohlcv(symbol, timeframe='1m', limit=self.ma_period)
        if not ohlcv or len(ohlcv) < self.ma_period:
            return False

        closes = [candle[4] for candle in ohlcv]
        ma = sum(closes) / len(closes)
        current_price = closes[-1]
        deviation = (current_price - ma) / ma

        # Kiểm tra sụt giá đột ngột
        if is_gap_too_large(current_price, self.last_price, self.gap_threshold_percent):
            print(f"[RiskControl] ❌ Cảnh báo GAP mạnh: {self.last_price} ➝ {current_price}")
            return False

        self.last_price = current_price

        print(f"[Reversal] Giá hiện tại: {current_price:.5f}, MA: {ma:.5f}, Độ lệch: {deviation:.2%}")
        if deviation < -self.threshold:
            tp, sl = calculate_tp_sl(current_price, TAKE_PROFIT_PERCENT, STOP_LOSS_PERCENT)
            print(f"🎯 Chốt lời dự kiến: {tp} USDT | 🛑 Cắt lỗ dự kiến: {sl} USDT")
            return True
        return False

    def check_stop_loss(self, entry_price, current_price):
        result = should_stop_loss(
            entry_price=entry_price,
            current_price=current_price,
            trade_amount=TRADE_AMOUNT,
            stop_loss_percent=STOP_LOSS_PERCENT,
            max_loss_usdt=self.max_loss_usdt
        )

        if result == "stop_loss":
            print("[STOP-LOSS] ❌ Dừng lỗ kích hoạt.")
        elif result == "exit_all":
            print("[MAX LOSS] ❌ Lỗ vượt ngưỡng tối đa! Cần đóng toàn bộ vị thế.")

        return result
