# Python Port Scanner

A multi-threaded TCP port scanner built in Python. Scans a target host over a configurable port range and reports which ports are open, using a thread pool for concurrent scanning.

## Features

- **Multi-threaded scanning** using `ThreadPoolExecutor` for fast, concurrent port checks
- **Object-oriented design** — scanning logic is encapsulated in a `PortScanner` class
- **Configurable via CLI** — set target, port range, thread count, and timeout without editing code
- **Timed output** — reports total scan duration

## How it works

For each port in the given range, the scanner attempts a TCP connection using Python's `socket` module. Rather than checking ports one at a time, it dispatches many connection attempts concurrently across a thread pool — since each check is mostly spent waiting on the network, overlapping the waits gives a large speedup over a sequential scan.

## Requirements

- Python 3.9+
- No external dependencies (uses only the standard library)

## Usage

\`\`\`bash
python port_scanner.py <target> [--start START] [--end END] [--threads THREADS] [--timeout TIMEOUT]
\`\`\`

**Example:**

\`\`\`bash
python port_scanner.py scanme.nmap.org --start 1 --end 1024 --threads 100
\`\`\`

**Arguments:**

| Argument     | Description                          | Default |
|--------------|---------------------------------------|---------|
| `target`     | Target IP address or hostname (required) | —    |
| `--start`    | Start of port range                   | 1       |
| `--end`      | End of port range                     | 1024    |
| `--threads`  | Max concurrent threads                | 100     |
| `--timeout`  | Socket timeout in seconds             | 0.5     |

**Sample output:**

\`\`\`
Scanning scanme.nmap.org — ports 1-1024 with 100 threads...

Open ports found:
  Port 22 is open
  Port 80 is open

Scan completed in 1.34 seconds.
\`\`\`

## ⚠️ Legal notice

Only scan hosts you own or have explicit permission to test, such as [scanme.nmap.org](http://scanme.nmap.org), which is publicly provided for this purpose. Scanning systems without authorization may violate computer-abuse laws in many countries.

## Possible extensions

- Banner grabbing to identify the service running on each open port
- Export results to CSV/JSON
- UDP scanning support

## Author

Priya Dharshni S
