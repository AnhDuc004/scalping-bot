# scalping-bot
# OKX Trading Bot (Python)

Bot giao dịch tự động trên sàn OKX sử dụng thư viện `ccxt`.

## Yêu cầu
- Python 3.8+
- Tài khoản OKX đã tạo API Key (vào [https://www.okx.com/account/my-api](https://www.okx.com/account/my-api))

## Cài đặt

```bash
git clone ...
cd your_project/
pip install -r requirements.txt
cp .env.example .env
# Sau đó điền thông tin vào file .env

# Run bot
python main.py

# Cấu trúc
okx_trading_bot/
├── main.py                      # Điểm khởi chạy bot chính, load env và thực thi chiến lược
├── okx_client.py               # Lớp giao tiếp với sàn OKX: kết nối API, đặt lệnh, lấy số dư...
├── strategy/                   # Thư mục chứa các chiến lược giao dịch
│   └── reversal_strategy.py    # Chiến lược đảo chiều đơn giản dựa trên MA
├── utils/                      # Các hàm helper hỗ trợ chiến lược (quản lý rủi ro, tính toán SL/TP)
│   └── risk_control.py         # Các hàm như kiểm tra dừng lỗ, khoảng cách giá, tính TP/SL
├── .env.example                # Mẫu file chứa biến môi trường: API key, chế độ demo/live
├── requirements.txt            # Danh sách thư viện Python cần cài đặt (ccxt, dotenv,...)
└── README.md                   # Hướng dẫn sử dụng, setup, chiến lược và cấu hình

