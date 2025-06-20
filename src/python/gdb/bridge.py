#!/usr/bin/env python3
"""
GDB Bridge - Allows Claude Code to interact with GDB programmatically.
"""

import subprocess
import time
import re
import json
from pathlib import Path

class GDBBridge:
    def __init__(self, binary_path="/usr/local/bin/2048"):
        self.binary = binary_path
        self.gdb_process = None
        self.board_address = None
        self.log_file = Path("logs/gdb_session.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
    def start(self):
        """Start GDB process."""
        print("🚀 Starting GDB...")
        self.gdb_process = subprocess.Popen(
            ["gdb", "-q", self.binary],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        time.sleep(0.5)
        
        # Initial setup
        self.send_command("set pagination off")
        self.send_command("set print pretty on")
        
    def send_command(self, cmd):
        """Send command to GDB and return output."""
        if not self.gdb_process:
            return None
            
        with open(self.log_file, 'a') as log:
            log.write(f"\n>>> {cmd}\n")
            
        self.gdb_process.stdin.write(cmd + "\n")
        self.gdb_process.stdin.flush()
        
        # Collect output (simple approach - may need refinement)
        time.sleep(0.1)
        output = ""
        
        # Read available output
        import select
        while True:
            ready, _, _ = select.select([self.gdb_process.stdout], [], [], 0.1)
            if ready:
                line = self.gdb_process.stdout.readline()
                output += line
                if "(gdb)" in line:
                    break
            else:
                break
                
        with open(self.log_file, 'a') as log:
            log.write(output)
            
        return output
    
    def find_board_pattern(self, pattern):
        """Search memory for a board pattern."""
        print(f"🔍 Searching for pattern: {pattern}")
        
        # Convert pattern to search command
        search_values = " ".join(str(v) for v in pattern)
        cmd = f"find /w 0x400000, 0x700000, {search_values}"
        
        output = self.send_command(cmd)
        
        # Parse addresses from output
        addresses = []
        for line in output.split('\n'):
            if "0x" in line:
                match = re.search(r'(0x[0-9a-fA-F]+)', line)
                if match:
                    addresses.append(match.group(1))
        
        return addresses
    
    def examine_memory(self, address, count=16):
        """Examine memory at address."""
        cmd = f"x/{count}wx {address}"
        output = self.send_command(cmd)
        
        # Parse values
        values = []
        for line in output.split('\n'):
            if "0x" in line and ":" in line:
                # Extract hex values after the colon
                parts = line.split(':')[1].strip().split()
                for part in parts:
                    if part.startswith('0x'):
                        values.append(int(part, 16))
        
        return values
    
    def verify_board_address(self, address):
        """Verify if address contains a valid game board."""
        values = self.examine_memory(address, 16)
        
        if len(values) != 16:
            return False
            
        # Check if it looks like a game board
        # - All values should be 0 or powers of 2
        # - Should have some zeros (empty cells)
        # - Should have some non-zeros (tiles)
        
        zeros = sum(1 for v in values if v == 0)
        powers_of_2 = sum(1 for v in values if v > 0 and (v & (v-1)) == 0)
        
        return zeros > 0 and zeros < 16 and (zeros + powers_of_2) == 16
    
    def set_ai_breakpoint(self):
        """Set breakpoint for AI intervention."""
        print("🎯 Setting AI breakpoint...")
        
        # Set breakpoint on input function
        self.send_command("break wgetch")
        
        # Add commands to call our AI
        commands = [
            "commands",
            "silent",
            "python",
            "# AI will be called here",
            "end",
            "end"
        ]
        
        for cmd in commands:
            self.send_command(cmd)

class Experiment:
    """Base class for experiments."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.results = {}
        
    def run(self, gdb_bridge):
        """Override in subclasses."""
        raise NotImplementedError
        
    def save_results(self):
        """Save experiment results."""
        output_dir = Path(f"experiments/{self.name}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / "results.json", 'w') as f:
            json.dump(self.results, f, indent=2)

class FindBoardExperiment(Experiment):
    """Experiment to find the game board in memory."""
    
    def __init__(self):
        super().__init__(
            "02-memory-search",
            "Find game board in memory using various strategies"
        )
        
    def run(self, gdb_bridge):
        print(f"\n🧪 Running experiment: {self.description}")
        
        # Start the game
        gdb_bridge.send_command("run")
        time.sleep(1)
        
        # Try to break and search
        gdb_bridge.send_command("Ctrl+C")  # This won't work - need different approach
        
        # Strategy 1: Search for common patterns
        strategies = [
            ("zeros", [0, 0, 0, 0]),
            ("small_values", [2, 0, 0, 2]),
            ("power_of_2", [16]),
            ("sequence", [0, 2, 4, 8])
        ]
        
        found_addresses = {}
        
        for name, pattern in strategies:
            print(f"\n  Strategy: {name}")
            addrs = gdb_bridge.find_board_pattern(pattern)
            found_addresses[name] = addrs
            print(f"    Found {len(addrs)} matches")
            
            # Check each address
            for addr in addrs[:5]:  # Check first 5
                values = gdb_bridge.examine_memory(addr, 16)
                if gdb_bridge.verify_board_address(addr):
                    print(f"    ✅ {addr} looks like a game board!")
                    self.results["board_address"] = addr
                    self.results["board_values"] = values
                    return
        
        self.results["search_results"] = found_addresses
        self.save_results()

# Main experiment runner
def run_experiments():
    """Run all experiments."""
    print("🔬 Claude Code GDB Experiment Runner")
    print("=" * 50)
    
    # First analyze source
    from analyze_2048_source import SourceAnalyzer
    analyzer = SourceAnalyzer()
    source_results = analyzer.analyze_all()
    
    # Start GDB
    bridge = GDBBridge()
    bridge.start()
    
    # Run experiments
    experiments = [
        FindBoardExperiment(),
    ]
    
    for exp in experiments:
        exp.run(bridge)
        
    print("\n✅ Experiments complete! Check experiments/ directory for results.")

if __name__ == "__main__":
    run_experiments()
