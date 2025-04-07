from dotenv import load_dotenv
import os
from exchange.okx_client import OKXClient
from strategies.scalping import ScalpingStrategy
from services.trade_manager import TradeManager

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy các giá trị API từ file .env
api_key = os.getenv('OKX_API_KEY')
secret_key = os.getenv('OKX_SECRET_KEY')
passphrase = os.getenv('OKX_PASSPHRASE')


# Tạo client và chạy bot
client = OKXClient(api_key, secret_key, passphrase, use_demo=True)
strategy = ScalpingStrategy(client)
manager = TradeManager(client, strategy)
manager.run()
