# Device Log Analyzer

A small Python command-line tool for parsing and analyzing device log files.

This project was built as part of preparation for a System Software Test & Development / SDET student role.  
It demonstrates practical work with logs, validation, error handling, automated testing, and command-line behavior.

---

## Project Goal

The goal of this project is to simulate a small automation/debugging tool that analyzes device logs.

The tool receives a log file, parses each line, validates the input format, and produces useful summaries such as:

- total number of logs
- number of logs by severity
- number of errors per device
- invalid log detection with clear error messages

This is intentionally a small project, but it demonstrates skills that are relevant to system software testing and development:

- reading logs
- parsing structured text
- validating inputs
- handling failure modes
- writing testable code
- testing at multiple levels
- checking CLI behavior through stdout, stderr, and exit codes

---

## Log Format

Each log line should follow this format:

```text
YYYY-MM-DD HH:MM:SS DEVICE_ID SEVERITY MESSAGE
```

Example:

```text
2026-06-04 12:01:03 DEVICE_1 INFO Started successfully
2026-06-04 12:02:10 DEVICE_1 ERROR Temperature too high
2026-06-04 12:03:00 DEVICE_2 WARNING Packet loss detected
2026-06-04 12:04:15 DEVICE_1 ERROR Fan failure
```

Supported severities:

```text
INFO
WARNING
ERROR
```

---

## Example Output

Running the tool on the sample log file:

```bash
python -m log_analyzer sample_logs/device.log
```

Expected output:

```text
Total logs: 4
INFO: 1
WARNING: 1
ERROR: 2

Errors by device:
DEVICE_1: 2
```

---

## Project Structure

```text
device-log-analyzer/
│
├── log_analyzer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── parser.py
│   └── analyzer.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_analyzer.py
│   ├── test_integration.py
│   └── test_cli.py
│
├── sample_logs/
│   └── device.log
│
├── README.md
└── pytest.ini
```

---

## Main Components

### `parser.py`

Responsible for parsing and validating log input.

Main functions:

```python
parse_log_line(line: str) -> dict
parse_log_file(file_path: str) -> list[dict]
```

Responsibilities:

- reject `None` input
- reject empty lines
- validate the timestamp format
- validate supported severity values
- preserve the full message, including spaces
- report invalid file lines with a line number

Example parsed result:

```python
{
    "timestamp": "2026-06-04 12:01:03",
    "device_id": "DEVICE_1",
    "severity": "INFO",
    "message": "Started successfully",
}
```

---

### `analyzer.py`

Responsible for analyzing parsed logs.

Main functions:

```python
count_by_severity(logs: list[dict]) -> dict
count_errors_by_device(logs: list[dict]) -> dict
find_critical_devices(logs: list[dict], threshold: int) -> list[str]
```

Responsibilities:

- count logs by severity
- count only `ERROR` logs per device
- identify devices with at least a given number of errors
- validate invalid thresholds

---

### `__main__.py`

Provides the CLI entry point.

Allows running the tool as:

```bash
python -m log_analyzer sample_logs/device.log
```

The CLI handles:

- missing arguments
- missing files
- invalid log files
- normal successful execution

It separates regular output and error output:

- normal results go to `stdout`
- errors go to `stderr`
- success returns exit code `0`
- failure returns exit code `1`

---

## How to Run

From the project root:

```bash
python -m log_analyzer sample_logs/device.log
```

---

## How to Run Tests

Install pytest if needed:

```bash
python -m pip install pytest
```

Run all tests:

```bash
python -m pytest
```

---

## Test Strategy

The project includes several levels of testing.

### 1. Unit Tests

Unit tests verify small functions in isolation.

Examples:

- `parse_log_line`
- `count_by_severity`
- `count_errors_by_device`
- `find_critical_devices`

These tests check that each function behaves correctly on its own.

---

### 2. Negative Tests

Negative tests verify that invalid inputs fail in a controlled and expected way.

Examples:

- empty log line
- `None` log line
- invalid timestamp format
- unsupported severity
- missing message
- invalid threshold
- missing file

The goal is not only to make the program work on valid input, but also to make sure it fails clearly on invalid input.

---

### 3. File-Based Tests

The parser is tested using temporary files through pytest's `tmp_path` fixture.

This keeps tests isolated and avoids depending on local files.

Example idea:

```text
create temporary log file -> parse file -> verify parsed logs
```

---

### 4. Integration Test

The integration test verifies that the output of the parser can actually be consumed by the analyzer.

Flow:

```text
raw log lines -> parser -> structured logs -> analyzer -> summary
```

This catches interface mismatches between components.

Example bug this could catch:

```python
{"level": "ERROR"}
```

instead of:

```python
{"severity": "ERROR"}
```

Even if each component has unit tests, the integration test ensures they work together.

---

### 5. CLI / System-ish Tests

The CLI is tested using `subprocess`.

These tests run the tool almost like a real user would.

They verify:

- return code
- stdout
- stderr
- valid input behavior
- missing argument behavior
- missing file behavior
- invalid log file behavior

Example checked behavior:

```text
valid file      -> exit code 0, summary in stdout, empty stderr
missing file    -> exit code 1, error in stderr
invalid log     -> exit code 1, line number in stderr
```

---

## Example Failure Handling

If a log file contains an invalid line, the tool reports the line number.

Example:

```text
Error: Invalid log line at line 2: Invalid log format
```

This makes debugging easier when analyzing larger files.

---

## Design Decisions

### Separation of Concerns

The project separates parsing from analysis:

```text
parser.py   -> converts raw text into structured data
analyzer.py -> computes statistics from structured data
```

This makes the code easier to test, debug, and extend.

---

### Clear Error Handling

Invalid inputs raise clear exceptions internally.

The CLI catches those exceptions and prints user-friendly error messages to `stderr`.

---

### `split(maxsplit=4)`

The parser uses:

```python
line.split(maxsplit=4)
```

instead of a regular `split()`.

Reason:

The message field may contain spaces.

Example:

```text
Temperature too high
```

Using `maxsplit=4` preserves the full message as one field.

---

### Exit Codes

The CLI returns meaningful exit codes:

```text
0 -> success
1 -> failure
```

This is important for automation, scripts, CI, and system-level tests.

---

## Current Status

Implemented:

- single-line parser
- full-file parser
- severity counter
- error counter by device
- critical device detection
- CLI entry point
- unit tests
- negative tests
- integration test
- CLI/system-ish tests

Possible future improvements:

- add CLI flags such as `--critical-threshold`
- support malformed-line skipping mode
- export output as JSON
- add more realistic sample logs
- add logging inside the tool
- add CI workflow
- package the project with `pyproject.toml`

---

## Useful Commands

Run the tool:

```bash
python -m log_analyzer sample_logs/device.log
```

Run tests:

```bash
python -m pytest
```

Run tests with verbose output:

```bash
python -m pytest -v
```
