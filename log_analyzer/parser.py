from datetime import datetime

VALID_SEVERITIES = {"INFO", "WARNING", "ERROR"}

def parse_log_line(line: str) -> dict:
    if line is None:
        raise ValueError("Log line cannot be None")
    
    line = line.strip()

    if not line:
        raise ValueError("Log line cannot be empty")
    
    parts = line.split(maxsplit=4)

    if len(parts) != 5:
        raise ValueError("Invalid log format")

    date_part, time_part, device_id, severity, message = parts

    timestamp = f"{date_part} {time_part}"

    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise ValueError("Invalid timestamp format") from exc
    
    if severity not in VALID_SEVERITIES:
        raise ValueError(f"Invalid severity: {severity}")
    
    if not message:
        raise ValueError("Message cannot be empty")
    
    return {
        "timestamp": timestamp,
        "device_id": device_id,
        "severity": severity,
        "message": message
    }

def parse_log_file(file_path: str) -> list[dict]:
    """
    Parse a log file into a list of structured log dictionaries.
    """
    if file_path is None:
        raise ValueError("File path cannot be None")

    parsed_logs = []

    with open(file_path, "r", encoding="utf-8") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            try:
                parsed_logs.append(parse_log_line(line))
            except ValueError as exc:
                raise ValueError(f"Invalid log line at line {line_number}: {exc}") from exc

    return parsed_logs