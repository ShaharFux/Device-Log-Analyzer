import pytest

from log_analyzer.analyzer import (
    count_by_severity,
    count_errors_by_device,
    find_critical_devices,
)


SAMPLE_LOGS = [
    {
        "timestamp": "2026-06-04 12:01:03",
        "device_id": "DEVICE_1",
        "severity": "INFO",
        "message": "Started successfully",
    },
    {
        "timestamp": "2026-06-04 12:02:10",
        "device_id": "DEVICE_1",
        "severity": "ERROR",
        "message": "Temperature too high",
    },
    {
        "timestamp": "2026-06-04 12:03:00",
        "device_id": "DEVICE_2",
        "severity": "WARNING",
        "message": "Packet loss detected",
    },
    {
        "timestamp": "2026-06-04 12:04:15",
        "device_id": "DEVICE_1",
        "severity": "ERROR",
        "message": "Fan failure",
    },
]


def test_count_by_severity():
    result = count_by_severity(SAMPLE_LOGS)

    assert result == {
        "INFO": 1,
        "ERROR": 2,
        "WARNING": 1,
    }


def test_count_by_severity_empty_logs():
    result = count_by_severity([])

    assert result == {}


def test_count_errors_by_device():
    result = count_errors_by_device(SAMPLE_LOGS)

    assert result == {
        "DEVICE_1": 2,
    }


def test_count_errors_by_device_no_errors():
    logs = [
        {
            "timestamp": "2026-06-04 12:01:03",
            "device_id": "DEVICE_1",
            "severity": "INFO",
            "message": "Started successfully",
        }
    ]

    result = count_errors_by_device(logs)

    assert result == {}


def test_find_critical_devices():
    result = find_critical_devices(SAMPLE_LOGS, threshold=2)

    assert result == ["DEVICE_1"]


def test_find_critical_devices_no_match():
    result = find_critical_devices(SAMPLE_LOGS, threshold=3)

    assert result == []


def test_find_critical_devices_invalid_threshold():
    with pytest.raises(ValueError):
        find_critical_devices(SAMPLE_LOGS, threshold=0)

def test_find_critical_devices():
    logs = [
        {"device_id": "A", "severity": "ERROR"},
        {"device_id": "A", "severity": "ERROR"},
        {"device_id": "B", "severity": "ERROR"},
    ]

    result = find_critical_devices(logs, 2)

    assert result == ["A"]

def test_find_critical_devices_threshold_boundary():
    logs = [
        {"device_id": "A", "severity": "ERROR"},
        {"device_id": "A", "severity": "ERROR"},
    ]

    result = find_critical_devices(logs, 2)

    assert result == ["A"]