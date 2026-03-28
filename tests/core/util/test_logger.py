import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from core.util.logger import LoggerFactory

def test_file_logger_write_file(tmp_path, monkeypatch):
    """
    File Logger Tests
    """
    log_file = tmp_path / "test.log"
    
    monkeypatch.setenv("LOG_FILE_PATH", str(log_file))
    monkeypatch.setenv("LOG_ENABLED", "1")
    
    logger_name = "TestApp"
    logger = LoggerFactory.create(logger_type="file", name=logger_name)
    
    log_text = "Log Text"
    logger.info(log_text)
    
    assert log_file.exists(), "FileLogger Not created the log file"
    
    with open(log_file, "r") as f:
        log_content = f.read()
        
    assert log_text in log_content
    assert "INFO" in log_content
    assert f"[{logger_name}]" in log_content
