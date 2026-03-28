# Principles of Data Science Portfolio Work

## Setup

```bash
pip install -r requirements.txt
cp .env .env
python app.py
```

## Env

```env
LOG_ENABLED=1

AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION_NAME=us-east-1
AWS_S3_BUCKET_NAME=your-bucket

START_DATE="2025-01-01"
END_DATE="2025-12-31"

YAHOO_FINANCE_TICKER="ETH-USD"
YAHOO_FINANCE_TICKERS="AAPL,GOOGL,MSFT,AMZN,META"
```

## Tests

```bash
pytest
pytest tests/core/util/test_logger.py  # specific test
```