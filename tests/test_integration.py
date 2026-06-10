from log_analyzer.parser import parse_log_line
from log_analyzer.analyzer import (
    count_by_severity,
    count_errors_by_device,
    find_critical_devices,
)


def test_parse_and_analyze_logs():
    raw_lines = [
        "2026-06-04 12:01:03 DEVICE_1 INFO Started successfully",
        "2026-06-04 12:02:10 DEVICE_1 ERROR Temperature too high",
        "2026-06-04 12:03:00 DEVICE_2 WARNING Packet loss detected",
        "2026-06-04 12:04:15 DEVICE_1 ERROR Fan failure",
    ]

    parsed_logs = [parse_log_line(line) for line in raw_lines]

    assert count_by_severity(parsed_logs) == {
        "INFO": 1,
        "ERROR": 2,
        "WARNING": 1,
    }

    assert count_errors_by_device(parsed_logs) == {
        "DEVICE_1": 2,
    }

    assert find_critical_devices(parsed_logs, threshold=2) == ["DEVICE_1"]