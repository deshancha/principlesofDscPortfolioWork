import os

class Logger:
    
    PREFIX = "LOG"

    COLORS = {
        "INFO": "\033[94m",    # B
        "WARN": "\033[93m",    # Y
        "ERROR": "\033[91m",   # R
        "VERBOSE": "\033[97m", # White
        "RESET": "\033[0m",
    }

    @classmethod
    def is_enabled(cls) -> bool:
        # Evaluated at runtime so that if you load .env later via python-dotenv, it still works.
        return os.environ.get("LOG_ENABLED", "0") == "1"

    @staticmethod
    def info(message: str):
        if Logger.is_enabled():
            print(f"{Logger.COLORS['INFO']}[INFO] {Logger.PREFIX}: {message}{Logger.COLORS['RESET']}")

    @staticmethod
    def warn(message: str):
        if Logger.is_enabled():
            print(f"{Logger.COLORS['WARN']}[WARN] {Logger.PREFIX}: {message}{Logger.COLORS['RESET']}")

    @staticmethod
    def error(message: str):
        if Logger.is_enabled():
            print(f"{Logger.COLORS['ERROR']}[ERROR] {Logger.PREFIX}: {message}{Logger.COLORS['RESET']}")

    @staticmethod
    def verbose(message: str):
        if Logger.is_enabled():
            print(f"{Logger.COLORS['VERBOSE']}[VERB] {Logger.PREFIX}: {message}{Logger.COLORS['RESET']}")
