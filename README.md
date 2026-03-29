# 📈 Binance Futures Testnet Trading Bot

A production-ready Python application designed to interact with the [Binance Futures Testnet](https://testnet.binancefuture.com) using the `python-binance` module. It features a highly modular core architecture, a professional Typer CLI, and a dynamic Streamlit UI Dashboard for seamlessly sending limit, market, and stop orders.

> **🎥 Watch the Video Demo**: [Click here to view the full application walkthrough on Google Drive](https://drive.google.com/file/d/1EGlFkgO06nuoU9W57CSDYGEFNpkt-E94/view?usp=sharing)

## ✨ Project Features & Requirements Met

This project was built adhering to the strict requirements of a senior Python application checkout:
- **Clean Architecture:** Core API connection (`client.py`), business logic (`orders.py`), input guardrails (`validators.py`), and decoupled custom Exceptions (`exceptions.py`).
- **3 Order Types Supported (Bonus):** `MARKET`, `LIMIT`, and `STOP` / `STOP_MARKET` all supported natively.
- **Enhanced CLI UX (Bonus):** Uses `Typer` and `Rich` to provide contextual, color-coded, interactive terminal prompts and visually stunning data tables. It requires affirmative `[y/N]` confirmation before touching the network.
- **Lightweight UI Dashboard (Bonus):** A dynamic `Streamlit` dashboard styled beautifully to simulate a premium SaaS trading terminal. Features real-time background log tracking directly in the browser!
- **Auto-Syncing Timestamps:** Mitigates the classic `Timestamp ahead of server` API error by automatically computing ping offsets during client initialization.
- **Structured Logging:** `logging_config.py` captures detailed chronological execution payloads strictly into `logs/trading_bot.log`. 

## ⚙️ Setup Instructions

### 1. Clone & Configure
Ensure you are in the directory where the bot code lives.

```bash
# We recommend creating a virtual environment:
python -m venv venv

# Windows Activation:
venv\Scripts\activate
# Mac/Linux Activation:
source venv/bin/activate

# Install all dependencies (python-binance, typer, streamlit, rich, etc.)
pip install -r requirements.txt
```

### 2. Generate Testnet API Keys
1. Log in to [Binance Futures Testnet](https://testnet.binancefuture.com/).
2. Look to the bottom of the execution interface, select the **API Key** tab, and generate a `System generated` key.
3. Rename the provided `.env.example` file to `.env` and fill in your keys:
   ```env
   BINANCE_API_KEY=your_generated_testnet_api_key
   BINANCE_API_SECRET=your_generated_testnet_secret
   ```

---

## 🚀 How to Run

### Command Line Interface (CLI)
*To see available commands and help options:*
```bash
python cli.py --help
```

**Example 1: Placing a MARKET Order**
```bash
python cli.py order BTCUSDT BUY MARKET 0.01
```

**Example 2: Placing a LIMIT Order (Requires limit price)**
```bash
python cli.py order BTCUSDT SELL LIMIT 0.05 --price 70000
```

*(You will be prompted for an interactive confirmation before any order is finalized, and given a formatted table containing order specifications for final review)*

### Web UI Dashboard (Streamlit)
Launch the interactive dashboard (this will open `http://localhost:8501` in your browser):
```bash
python -m streamlit run ui.py
```

---

## 💻 Example Expected Outcomes

### CLI Execution Output
```text
Order Summary
-------------
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01

Do you want to proceed with placing this order? [y/N]: y

(Spinning animation...) Placing order on Binance Testnet...

╭──────────────────────────────── API Success Response ─────────────────────────────────╮
│ Order Placed Successfully!                                                            │
│                                                                                       │
│ {                                                                                     │
│   "orderId": 128493821,                                                               │
│   "status": "NEW",                                                                    │
│   "executedQty": "0",                                                                 │
│   "avgPrice": "0"                                                                     │
│ }                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────╯
```

### Log File Tracking (`logs/trading_bot.log`)
```log
2026-03-29 14:12:05 | INFO     | config     | Attempting to validate `.env` keys.
2026-03-29 14:12:05 | INFO     | client     | Initialized python-binance Testnet Client.
2026-03-29 14:12:05 | INFO     | orders     | Validating inputs for: BUY 0.01 BTCUSDT @ MARKET (Price=None)
2026-03-29 14:12:06 | INFO     | client     | Successfully pinged Binance Futures Testnet API.
2026-03-29 14:12:06 | INFO     | client     | Sending order request payload: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
2026-03-29 14:12:07 | INFO     | client     | Order successful! Response: {...}
```

---

## 📝 Assumptions & Disclaimers

1. **Testnet Strictness:** Designed specifically for `https://testnet.binancefuture.com` (USDT-M). Production mainnet keys will securely and intentionally fail initialization.
2. **Pairs:** Optimized primarily for generic USDT pairs (e.g., `BTCUSDT`).
3. **Execution Fills:** Because this evaluates on the Testnet sandbox, `LIMIT` requests and `STOP` losses depend entirely on Testnet mock liquidity volume to eventually fill (though they will successfully hit the orderbook as `NEW`).
4. **Environment Variables:** This project strictly enforces `python-dotenv` and strongly assumes the user/reviewer understands to place their credentials securely in `.env` rather than hardcoding them into executable files.
