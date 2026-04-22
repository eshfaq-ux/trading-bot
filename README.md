# Binance Spot Testnet Trading Bot

A Python trading bot with both a CLI and a web UI to place orders on the [Binance Spot Testnet](https://testnet.binance.vision).

> **Note:** The Binance Futures Testnet (`testnet.binancefuture.com`) was taken offline by Binance as part of an ongoing upgrade ([official announcement](https://www.binance.com/en/support/announcement/detail/616402d041c74000bc78282018bc62d4)). This bot uses the Binance Spot Testnet which has an identical API structure, authentication mechanism, and order types.

---

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # Binance REST client (HMAC signing, requests)
    orders.py          # Order placement logic
    validators.py      # Input validation
    logging_config.py  # Logging setup
  templates/
    index.html         # Cyber neon web UI
  cli.py               # CLI entry point
  app.py               # Flask web UI entry point
  requirements.txt
  README.md
  trading_bot.log
```

---

## Setup

### 1. Get Testnet API Credentials

1. Go to [https://testnet.binance.vision](https://testnet.binance.vision)
2. Log in with GitHub
3. Click **"Generate HMAC-SHA-256 Key"**
4. Save the API Key and Secret immediately (shown only once)

### 2. Install Dependencies

```bash
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Set API Credentials

```powershell
# Windows PowerShell
$env:BINANCE_API_KEY="your_api_key"
$env:BINANCE_API_SECRET="your_api_secret"
```

```bash
# Linux/Mac
export BINANCE_API_KEY=your_api_key
export BINANCE_API_SECRET=your_api_secret
```

---

## How to Run

### Option A — CLI

```bash
# MARKET order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# LIMIT order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000

# STOP_LOSS_LIMIT order (bonus)
python cli.py --symbol BTCUSDT --side SELL --type STOP_LOSS_LIMIT --quantity 0.001 --price 75000
```

### Option B — Web UI

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## CLI Output Example

```
── Order Request ──────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
───────────────────────────────────────────

── Order Response ─────────────────────────
  Order ID   : 7985927
  Status     : FILLED
  Executed   : 0.00100000
───────────────────────────────────────────

✅  Order placed successfully.
```

---

## Logging

All API requests, responses, and errors are logged to `trading_bot.log`.

- File: `DEBUG` level (full request/response bodies)
- Console: `WARNING` level (errors only)

---

## Assumptions

- Uses Binance Spot Testnet (`https://testnet.binance.vision`) due to Futures Testnet being offline
- `STOP_LOSS_LIMIT` uses `--price` as both the stop trigger and limit price
- No position/balance management — order placement only
