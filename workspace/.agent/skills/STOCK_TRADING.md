---
description: Execute stock trading and analysis via KIS API.
---

# 📈 Stock Trading Skill (KIS)

Korean Investment & Securities (KIS) API integration for automated trading and market analysis.

## Overview
This skill grants the agent the ability to access real-time stock market data, manage portfolios, and execute buy/sell orders through the Korea Investment & Securities (KIS) OpenAPI.

## Key Capabilities
- **Analysis**: Retrieve current prices (`get_current_price`), order books, and market trends.
- **Trading**: Execute `buy` and `sell` orders (Market/Limit).
- **Portfolio**: Check account balance (`get_balance`) and current positions (`get_positions`).

## Locations
- Engine: `E:\stock\backend\app\tools\kis_client.py`
- Configuration: `E:\stock\backend\.env`
