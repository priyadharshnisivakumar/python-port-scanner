import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
 
 
class PortScanner:
    """Scans a target host over a range of ports using a thread pool."""
 
    def __init__(self, target: str, start_port: int = 1, end_port: int = 1024,
                 timeout: float = 0.5, max_threads: int = 100):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.max_threads = max_threads
        self.open_ports = []
 
    def scan_port(self, port: int) -> int | None:
        """Attempt to connect to a single port. Returns the port if open, else None."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    return port
        except socket.error:
            pass
        return None
 
    def run(self) -> list[int]:
        """Scan the full port range concurrently using a thread pool."""
        ports = range(self.start_port, self.end_port + 1)
 
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self.scan_port, port): port for port in ports}
 
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    self.open_ports.append(result)
 
        self.open_ports.sort()
        return self.open_ports
 
 
def main():
    parser = argparse.ArgumentParser(description="Multi-threaded TCP port scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("--threads", type=int, default=100, help="Max concurrent threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Socket timeout in seconds (default: 0.5)")
    args = parser.parse_args()
 
    print(f"Scanning {args.target} — ports {args.start}-{args.end} "
          f"with {args.threads} threads...\n")
 
    scanner = PortScanner(
        target=args.target,
        start_port=args.start,
        end_port=args.end,
        timeout=args.timeout,
        max_threads=args.threads,
    )
 
    start_time = time.time()
    open_ports = scanner.run()
    elapsed = time.time() - start_time
 
    if open_ports:
        print("Open ports found:")
        for port in open_ports:
            print(f"  Port {port} is open")
    else:
        print("No open ports found in the given range.")
 
    print(f"\nScan completed in {elapsed:.2f} seconds.")
 
 
if __name__ == "__main__":
    main()
