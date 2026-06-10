from collections import Counter


def count_by_severity(logs: list[dict]) -> dict:
    """
    Count log entries by severity.
    """
    counter = Counter()

    for log in logs:
        severity = log["severity"]
        counter[severity] += 1

    return dict(counter)


def count_errors_by_device(logs: list[dict]) -> dict:
    """
    Count ERROR logs per device.
    """
    counter = Counter()

    for log in logs:
        if log["severity"] == "ERROR":
            device_id = log["device_id"]
            counter[device_id] += 1

    return dict(counter)


def find_critical_devices(logs: list[dict], threshold: int) -> list[str]:
    """
    Return devices with at least `threshold` ERROR logs.
    """
    if threshold <= 0:
        raise ValueError("Threshold must be positive")

    errors_by_device = count_errors_by_device(logs)

    return [
        device_id
        for device_id, error_count in errors_by_device.items()
        if error_count >= threshold
    ]

def get_error_logs(logs: list[dict]) -> list[dict]:
    """
    Return all logs with ERROR severity.
    """
    return [
        log
        for log in logs
        if log["severity"] == "ERROR"
    ]