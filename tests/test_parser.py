import pytest

from log_analyzer.parser import parse_log_line, parse_log_file

def test_parse_valid_info_log_line():
    line = "2026-06-04 12:01:03 DEVICE_01 INFO Started successfully"

    result = parse_log_line(line)

    assert result == {
        "timestamp": "2026-06-04 12:01:03",
        "device_id": "DEVICE_01",
        "severity": "INFO",
        "message": "Started successfully"
    }

def test_parse_valid_error_log_line():
    line = "2026-06-04 12:01:03 DEVICE_01 ERROR Temperature too high"

    result = parse_log_line(line)

    assert result == {
        "timestamp": "2026-06-04 12:01:03",
        "device_id": "DEVICE_01",
        "severity": "ERROR",
        "message": "Temperature too high"
    }

def test_empty_line_raises_error():
    with pytest.raises(ValueError):
        parse_log_line("")

def test_invalid_severity_raises_error():
    line = "2026-06-04 12:01:03 DEVICE_01 NORMAL Started successfully"
    with pytest.raises(ValueError):
        parse_log_line(line)

def test_invalid_timestamp_format_raises_error():
    line = "2026/06/04 12:01:03 DEVICE_1 INFO Started successfully"

    with pytest.raises(ValueError):
        parse_log_line(line)

def test_missing_message_raises_error():
    line = "2026-06-04 12:01:03 DEVICE_1 INFO"

    with pytest.raises(ValueError):
        parse_log_line(line)

def test_none_line_raises_error():
    with pytest.raises(ValueError):
        parse_log_line(None)

def test_parse_log_file_valid_file(tmp_path):
    log_file = tmp_path / "device.log"
    log_file.write_text(
        "2026-06-04 12:01:03 DEVICE_1 INFO Started successfully\n"
        "2026-06-04 12:02:10 DEVICE_1 ERROR Temperature too high\n",
        encoding="utf-8",
    )

    result = parse_log_file(str(log_file))

    assert len(result) == 2
    assert result[0]["severity"] == "INFO"
    assert result[1]["severity"] == "ERROR"


def test_parse_log_file_invalid_line_includes_line_number(tmp_path):
    log_file = tmp_path / "device.log"
    log_file.write_text(
        "2026-06-04 12:01:03 DEVICE_1 INFO Started successfully\n"
        "bad line\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="line 2"):
        parse_log_file(str(log_file))


def test_parse_log_file_empty_file(tmp_path):
    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")

    result = parse_log_file(str(log_file))

    assert result == []