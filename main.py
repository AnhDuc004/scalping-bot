from dotenv import load_dotenv
import os
from exchange.okx_client import OKXClient
from strategies.reversal import ReversalStrategy   # 🔁 đổi từ scalping sang reversal
from services.trade_manager import TradeManager

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy các giá trị API từ file .env
api_key = os.getenv('OKX_API_KEY')
secret_key = os.getenv('OKX_SECRET_KEY')
passphrase = os.getenv('OKX_PASSPHRASE')

# Tạo client và chạy bot
client = OKXClient(api_key, secret_key, passphrase, use_demo=True) # Chạy trên môi trường demo (sandbox) / tắt demo giao dịch thật (LIVE) => False
strategy = ReversalStrategy(client)    # đổi chiến lược (scalping sang reversal hoặc ... nếu a có thêm chiến lược khác)
manager = TradeManager(client, strategy)
manager.run()
