import subprocess
import sys


def test_cli_valid_log_file(tmp_path):
    log_file = tmp_path / "device.log"
    log_file.write_text(
        "2026-06-04 12:01:03 DEVICE_1 INFO Started successfully\n"
        "2026-06-04 12:02:10 DEVICE_1 ERROR Temperature too high\n"
        "2026-06-04 12:03:00 DEVICE_2 WARNING Packet loss detected\n"
        "2026-06-04 12:04:15 DEVICE_1 ERROR Fan failure\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "log_analyzer", str(log_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Total logs: 4" in result.stdout
    assert "INFO: 1" in result.stdout
    assert "WARNING: 1" in result.stdout
    assert "ERROR: 2" in result.stdout
    assert "DEVICE_1: 2" in result.stdout
    assert result.stderr == ""


def test_cli_missing_argument():
    result = subprocess.run(
        [sys.executable, "-m", "log_analyzer"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "usage:" in result.stderr


def test_cli_file_not_found():
    result = subprocess.run(
        [sys.executable, "-m", "log_analyzer", "missing.log"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "file not found" in result.stderr


def test_cli_invalid_log_file(tmp_path):
    log_file = tmp_path / "bad.log"
    log_file.write_text(
        "2026-06-04 12:01:03 DEVICE_1 INFO Started successfully\n"
        "bad line\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "log_analyzer", str(log_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "line 2" in result.stderr

def test_cli_custom_critical_threshold(tmp_path):
    log_file = tmp_path / "critical.log"
    log_file.write_text(
        "2026-06-04 12:01:00 DEVICE_1 ERROR Temperature too high\n"
        "2026-06-04 12:02:00 DEVICE_1 ERROR Fan failure\n"
        "2026-06-04 12:03:00 DEVICE_1 ERROR Shutdown required\n"
        "2026-06-04 12:04:00 DEVICE_2 ERROR Packet loss\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "log_analyzer",
            str(log_file),
            "--critical-threshold",
            "3",
        ],
        capture_output=True,
        text=True,
    )

    critical_section = result.stdout.split("Critical devices:")[1]

    assert result.returncode == 0
    assert "Critical devices:" in result.stdout
    assert "DEVICE_1" in critical_section
    assert "DEVICE_2" not in critical_section
    assert result.stderr == ""

def test_cli_show_errors(tmp_path):
    log_file = tmp_path / "errors.log"
    log_file.write_text(
        "2026-06-04 12:01:00 DEVICE_1 INFO Started successfully\n"
        "2026-06-04 12:02:00 DEVICE_1 ERROR Temperature too high\n"
        "2026-06-04 12:03:00 DEVICE_2 WARNING Packet loss detected\n"
        "2026-06-04 12:04:00 DEVICE_3 ERROR Fan failure\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "log_analyzer",
            str(log_file),
            "--show-errors",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Error logs:" in result.stdout
    assert "DEVICE_1: Temperature too high" in result.stdout
    assert "DEVICE_3: Fan failure" in result.stdout
    assert "Started successfully" not in result.stdout
    assert "Packet loss detected" not in result.stdout
    assert result.stderr == ""

def test_cli_invalid_critical_threshold(tmp_path):
    log_file = tmp_path / "critical.log"
    log_file.write_text(
        "2026-06-04 12:01:00 DEVICE_1 ERROR Temperature too high\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "log_analyzer",
            str(log_file),
            "--critical-threshold",
            "0",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Threshold must be positive" in result.stderr