from config import SPREAD_THRESHOLD

class ScalpingStrategy:
    def __init__(self, client):
        self.client = client

    def should_enter_trade(self, symbol):
        bid, ask = self.client.get_price(symbol)
        spread = ask - bid
        print(f"[Spread Check] Bid: {bid} - Ask: {ask} - Spread: {spread}")
        return spread < SPREAD_THRESHOLD
