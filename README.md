## Project Setup

Project used Python for programming, and a virtual environment to manage
dependencies.

1: Create Virtual Environment

    python3 -m venv .venv

2: Activate Virtual Environment

    source .venv/bin/activate 

3: Install Dependencies

    pip install -r requirements.txt

4: Environment Variables

Create a `.env` file at the root directory to setting up the
configurations.

    YAHOO_FINANCE_TICKERS="BTC-USD,ETH-USD,SOL-USD,BNB-USD,DOGE-USD"
    START_DATE="2020-01-01"
    END_DATE="2026-03-31"

    AWS_REGION_NAME="us-east-1"
    AWS_S3_BUCKET_NAME[aws-s3-bucket-name]"
    AWS_RDS_TABLE_NAME="[aws-aurora-rds-table-name]"

    DB_CONNECTION_STRING="mysql+pymysql://[username]:[password]@[host]:[port]/[database-name]"

## Project Architecture

> This project was built focusing on scalability and separation.

## Clean Architecture

> The code adheres to clean architecture principles and separated
> between domain and data layers.\
> \
> **domain**: models, abstract managers, usecases\
> **data**: manager implementation

## Dependency Injection

> By using a `dependency`` ``injector` all services instantiated inside
> `AppContainer`. This ensures dependency flow decouples via interfaces.
> This would make the atchitecture more future proof and allow mock
> injection for testing.

## Modularized

## Source is modularized for separate distinct modules. {#source-is-modularized-for-separate-distinct-modules. .unnumbered}

+---------------------+------------------------------------------------+
| Module Root         | Description                                    |
+=====================+================================================+
| **src/core**        | Core components like (AWS S3/RDS Managers),    |
|                     | utilities like logger, core module formatted   |
|                     | log strings                                    |
+---------------------+------------------------------------------------+
| **sr                | ## Infrastructure laye                         |
| c/data_collection** | r implementing data fetching, uploading and lo |
|                     | ading with operations like below defined as us |
|                     | ecases {#infrastructure-layer-implementing-dat |
|                     | a-fetching-uploading-and-loading-with-operatio |
|                     | ns-like-below-defined-as-usecases .unnumbered} |
|                     |                                                |
|                     | -   Collect yahoo finance market data          |
|                     |                                                |
|                     | -   Upload to AWS S3                           |
|                     |                                                |
|                     | -   Download from AWS S3                       |
|                     |                                                |
|                     | -   AWS S3 to AWS RDS                          |
|                     |                                                |
|                     | -   AWS RDS to Pandas                          |
|                     |                                                |
|                     | -   AWS RDS Cleanup                            |
+---------------------+------------------------------------------------+
| **src/agent**       | ## Contains the agent wor                      |
|                     | kflow divided in to function modules as compon |
|                     | ents {#contains-the-agent-workflow-divided-in- |
|                     | to-function-modules-as-components .unnumbered} |
|                     |                                                |
|                     | -   CoinAnalysisModule                         |
|                     |                                                |
|                     | -   MockNewsItemModule                         |
|                     |                                                |
|                     | -   DecisionModule                             |
+---------------------+------------------------------------------------+

## Threading

> Pulling large different types of data sets from Yahoo Finance API and
> transmitting them to AWS S3 introduces delays. By using asynchronous
> methods increase the transmission time significantly.

##  {#section .unnumbered}

## Logger

>     Shared Logger component for logging in the application.
>
>     This can be disabled with .env configuration

## Data Collection

Related Configuration in .env


    Collected following five crypto currency coins USD rates details from Yahoo finance Data

a.  BitCoin - BTC

b.  Ethereum - ETH

c.  Solana - SOL

d.  Build and Build - BNB

e.  Dogecoin - DOGE

```{=html}
<!-- -->
```
    Following components has been implemented 

1.  Download yfinance tickers configured in “YAHOO_FINANCE_TICKERS” env var between “START_DATE” and “END_DATE” and upload to AWS S3 as json

2.  Save all the configured tickers them inside AWS RDS table

3.  Load pandas dataframes from AWS RDS configured in “YAHOO_FINANCE_TICKERS”

## Execution with CMD Args  {#execution-with-cmd-args .unnumbered}

    python app.py [arg]

+----------+------------------+----------------------------------------+
| Argument | Description      | Action                                 |
+==========+==================+========================================+
| `-1`     | Drop/Cleanup     | -   Execute DataCleaningUseCase.       |
|          | Data             | -   Drops test tables in RDS.          |
+----------+------------------+----------------------------------------+
| `1`      | YFinace Put to   | -   Execute                            |
|          | S3               |     FetchParallelAndUploadToS3UseCase  |
|          |                  | -   Fetch Yahoo Finance data from      |
|          |                  |     specified `.env` tickers           |
|          |                  |     asynchronously and put the raw     |
|          |                  |     JSON into AWS S3.                  |
+----------+------------------+----------------------------------------+
| `2`      | S3 to RDS        | -   Execute S3ToRDSUseCase             |
|          |                  | -   Pulls the JSON from AWS S3.        |
|          |                  | -   Structures them into relational    |
|          |                  |     data format                        |
|          |                  | -   Save to AWS RDS relational         |
|          |                  |     database table                     |
+----------+------------------+----------------------------------------+
| `3`      | Extract to       | -   Execute RDSToPandasUseCase         |
|          | Pandas           | -   Extracts market data from AWS RDS  |
|          |                  | -   Load them to Pandas DataFrame      |
+----------+------------------+----------------------------------------+

##  {#section-1 .unnumbered}

## EDA - Data Cleaning

This is demonstrated in two Jupyter note book file

1.  eda_data_cleaning_single.ipynb

> Data Clean up Step by Step for targeted Yahoo Finance Ticker

2.  eda_data_cleaning_all.ipynb

> Execute Clean up for All configured tickers using the
> "data_cleaning_usecase" usecase

**Steps 1**: Meaningful Rename and Drop the Columns Not need

**Step 2**: Handle Missing Values with forward filling

Notes : No missing values found for any coin

**Step 2**: Convert Data Types

Volume column were identified as object and converted to number.

Step 4: Line Chart

## EDA -- Feature Engineering and Clustering

> We use trade price **Percentage change day over day** for clustering
> algorithm because of following reasons

1.  Crypto currency trade in different scales.\
    > Eg: Bitcoin trads in thousands of dollars but Doge trades in
    > fraction of dollar.

2.  If closing price were fed to K-Means the model would be heavily
    > biased,\
    > Eg: expensive vs cheap coins

3.  Daily percentage change would normalize the dataset and allows equal
    > weight for comparison

> Standard Deviation of daily close value used for acting as the
> **risk** factor.

We pick K as 3 to fit into 3 clusters which possibly interpret as
following types

a.  High Rist

b.  Medium Risk

c.  Low Risk

## Result {#result .unnumbered}

## Crypto Coins Volatility {#crypto-coins-volatility .unnumbered}

BTC -- 0.025 Lowest STD Daily Close (Lowest Volatility)\
BNB -- 0.028 Very Low Volatility\
ETH -- 0.037 Moderate Volatility\
SOL -- 0.043 High Volatility\
DOGE -- 0.05 Highest Volatility

##   Crypto Coins Clusters  {#crypto-coins-clusters .unnumbered}

1.  Low Risk -- BTC and BNB

2.  Medium Risk -- ETH and SOL

3.  High Risk -- DOGE

## Trading Agent

Following components has been implemented to show case agentic AI
workflow

1.  **Coin Analysis
    (src/agent/domain/components/**`coin_analysis.py`**)**

> Based on Clustering/volatility insights above the coins were assigned
> to risk categories and agent returns the details

2.  **Information Retrieval
    (src/agent/domain/components/**`information_retrieval.py`**)**

> Simulates an RAG (Retrieval Augmented Generation) pipeline. Simply
> mock the market sentiment (Bullish vs. Bearish) for the coins.

3.  **Decision Module
    (src/agent/domain/components/**`decision_module.py`**)**

> Simulates LLM Agentic Decisions by getting the sentiment and returns
> BUY or SELL decision.

4.  **Decision Evaluate
    (src/agent/domain/components/**`dicision_evaluate.py`**)**

> Simulate the risk manager. Based on the decision module output this
> determines the portion of capital to be spent for a coin based on its
> cluster.
>
> (ex: allocating capital for low-risk coins, but limiting spending on
> high-risk coins)

Execution of Trading Agent


    python app.py 4
