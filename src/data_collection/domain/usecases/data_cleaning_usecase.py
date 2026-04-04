# Author: Chamika Deshan
# Created: 2026-04-01

import pandas as pd
import numpy as np
from core.util import ILogger
from core.util.messages import LogMessages

class DataCleaningUseCase:
    
    def __init__(self, logger: ILogger):
        self.logger = logger

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Start data cleaning")
        
        if df is None or df.empty:
            self.logger.error("DataFrame is empty")
            return None

        # Drop source
        if 'source' in df.columns:
            df = df.drop(columns=['source'])
            self.logger.info("Dropped 'source' column.")

        # Rename columns
        rename_map = {
            'timestamp_utc': 'date',
            'open_price': 'open',
            'high_price': 'high',
            'low_price': 'low',
            'close_price': 'close'
        }
        df = df.rename(columns=rename_map)
        self.logger.info(f"Columns after renaming: {df.columns.tolist()}")

        # Handle Missing Values
        initial_missing = df.isnull().sum().sum()
        if initial_missing > 0:
            self.logger.info(f"Handling {initial_missing} missing values")
            df = df.fillna(method='ffill')
        
        # Looks not need but convert Date column type
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Only volume need but jsut convert all
        numeric_cols = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        cleaned_missing = df.isnull().sum().sum()
        self.logger.info(f"Data cleaning complete. Missing: {cleaned_missing}")
        
        return df
