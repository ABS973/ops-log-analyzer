# ops-log-analyzer

> Parse structured log files into a JSON summary and a human-readable incident report — in one Python script.

---

## What It Does

`log_report_l4.py` reads a pipe-delimited log file and produces two outputs:

| Output | Format | Use case |
|---|---|---|
| `summary_l4.json` | Machine-readable | Dashboards, alerting tools, CI checks |
| `incident_report_l4.txt` | Human-readable | Tickets, Slack, email escalations |

---

## Log Format Expected

Each line must follow this structure:

```
YYYY-MM-DD HH:MM:SS | LEVEL | service | message
```

Example:

```
2026-02-05 08:11:20 | ERROR | api | Unhandled exception
2026-02-05 08:11:21 | INFO  | auth | User login success
2026-02-05 08:11:22 | WARN  | api | Slow response
```

Malformed lines (missing separators, unknown levels) are skipped gracefully and counted in a footer note.

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/<your-username>/ops-log-analyzer.git
cd ops-log-analyzer

# Place your log file in the project root
mv your-logs.txt clean_logs_l4.txt

# Run
python log_report_l4.py
```

No dependencies — standard library only (`json`, `open`).

---

## Output Examples

**`summary_l4.json`**

```json
{
  "level_counts": {
    "INFO": 35253,
    "WARN": 9814,
    "ERROR": 3922
  },
  "service_counts": {
    "api": 4821,
    "db": 3104,
    "auth": 2987
  }
}
```

**`incident_report_l4.txt`**

```
INCIDENT MINI-REPORT
========================================

INFO: 35253
WARN: 9814
ERROR: 3922

Top services:
  storage: 2533
  profile: 2532
  billing: 2524

Sample ERROR logs:
  2026-02-01 00:15:43 | ERROR | inventory | Write operation failed: storage quota exceeded
  2026-02-01 00:15:46 | ERROR | cache | Service dependency not responding dependency=stripe
```

---

## Project Structure

```
ops-log-analyzer/
├── log_report_l4.py        # Main script
├── clean_logs_l4.txt       # Input log file (you provide this)
├── summary_l4.json         # Generated — JSON summary
├── incident_report_l4.txt  # Generated — incident report
└── README.md
```

---

## How It Works

1. Reads `clean_logs_l4.txt` line by line
2. Splits each line on `|` and strips whitespace
3. Counts occurrences per log level and per service using dicts
4. Collects up to 5 sample `ERROR` lines as evidence
5. Writes the JSON summary with `json.dump(indent=2)`
6. Writes the text report with f-strings and `open(..., "w")`

---

## Developed In

GitHub Codespaces — no local setup required.

---

## License

MIT
