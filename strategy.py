# class ReversalStrategy:
#     def __init__(self, client, ma_period=20, threshold=0.002):
#         self.client = client
#         self.ma_period = ma_period
#         self.threshold = threshold

#     def should_enter_trade(self, symbol):
#         ohlcv = self.client.fetch_ohlcv(symbol, timeframe='1m', limit=self.ma_period)
#         if not ohlcv or len(ohlcv) < self.ma_period:
#             return False

#         closes = [candle[4] for candle in ohlcv]
#         ma = sum(closes) / len(closes)
#         current_price = closes[-1]
#         deviation = (current_price - ma) / ma

#         print(f"[Reversal] Giá hiện tại: {current_price:.5f}, MA: {ma:.5f}, Độ lệch: {deviation:.5%}")

#         return deviation < -self.threshold
