import argparse
import sys

from log_analyzer.analyzer import (
    count_by_severity,
    count_errors_by_device,
    find_critical_devices,
    get_error_logs
)
from log_analyzer.parser import parse_log_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze device log files"
    )

    parser.add_argument(
        "log_file",
        help="Path to the log file"
    )

    parser.add_argument(
        "--critical-threshold",
        type=int,
        default=3,
        help="Number of ERROR logs required to mark a device as critical"
    )

    parser.add_argument(
    "--show-errors",
    action="store_true",
    help="Print all ERROR log messages"
    )

    args = parser.parse_args()

    try:
        logs = parse_log_file(args.log_file)
        critical_devices = find_critical_devices(
            logs,
            args.critical_threshold
        )
    except FileNotFoundError:
        print(f"Error: file not found: {args.log_file}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    severity_counts = count_by_severity(logs)
    errors_by_device = count_errors_by_device(logs)

    print(f"Total logs: {len(logs)}")
    print(f"INFO: {severity_counts.get('INFO', 0)}")
    print(f"WARNING: {severity_counts.get('WARNING', 0)}")
    print(f"ERROR: {severity_counts.get('ERROR', 0)}")

    print()
    print("Errors by device:")

    if errors_by_device:
        for device_id, count in errors_by_device.items():
            print(f"{device_id}: {count}")
    else:
        print("None")

    print()
    print("Critical devices:")

    if critical_devices:
        for device_id in critical_devices:
            print(device_id)
    else:
        print("None")

    if args.show_errors:
        error_logs = get_error_logs(logs)

        print()
        print("Error logs:")

        if error_logs:
            for log in error_logs:
                print(f"{log['device_id']}: {log['message']}")
        else:
            print("None")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())