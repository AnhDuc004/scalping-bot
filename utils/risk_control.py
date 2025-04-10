def is_gap_too_large(current_price, last_price, gap_threshold_percent):
    if not last_price:
        return False
    change = abs((current_price - last_price) / last_price) * 100
    return change >= gap_threshold_percent

def should_stop_loss(entry_price, current_price, trade_amount, stop_loss_percent, max_loss_usdt):
    sl_price = entry_price * (1 - stop_loss_percent / 100)
    if current_price <= sl_price:
        estimated_loss = (entry_price - current_price) * trade_amount
        if estimated_loss >= max_loss_usdt:
            return "exit_all"
        else:
            return "stop_loss"
    return None
def calculate_tp_sl(entry_price, take_profit_percent, stop_loss_percent):
    take_profit_price = entry_price * (1 + take_profit_percent / 100)
    stop_loss_price = entry_price * (1 - stop_loss_percent / 100)
    return round(take_profit_price, 5), round(stop_loss_price, 5)

