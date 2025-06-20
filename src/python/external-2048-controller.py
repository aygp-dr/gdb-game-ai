#!/usr/bin/env python3
"""
External controller that runs GDB as subprocess.
Works even without Python/Guile support in GDB.
"""

import subprocess
import time
import re
import sys

class External2048Controller:
    def __init__(self):
        self.gdb = None
        self.board_address = None
        
    def start(self):
        """Start GDB with 2048."""
        print("🚀 Starting GDB with 2048...")
        self.gdb = subprocess.Popen(
            ['gdb', '-q', '/usr/local/bin/2048'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0
        )
        
        # Wait for GDB prompt
        self._wait_for_prompt()
        
        # Start the game
        self._send_command("run")
        time.sleep(2)  # Let game initialize
        
    def _send_command(self, cmd):
        """Send command to GDB."""
        print(f">>> {cmd}")
        self.gdb.stdin.write(cmd + "\n")
        self.gdb.stdin.flush()
        
    def _wait_for_prompt(self):
        """Wait for GDB prompt."""
        output = ""
        while True:
            char = self.gdb.stdout.read(1)
            output += char
            if output.endswith("(gdb) "):
                break
        return output
        
    def interrupt_game(self):
        """Send Ctrl+C to GDB."""
        print("🛑 Interrupting game...")
        self.gdb.send_signal(subprocess.signal.SIGINT)
        time.sleep(0.5)
        
    def find_board(self):
        """Find the game board."""
        print("🔍 Searching for board...")
        
        # Search for common patterns
        self._send_command("find /w 0x400000, 0x700000, 0, 0, 0, 2")
        output = self._wait_for_prompt()
        
        # Parse addresses
        addresses = re.findall(r'(0x[0-9a-fA-F]+)', output)
        
        for addr in addresses:
            # Check if it's a valid board
            self._send_command(f"x/16wx {addr}")
            output = self._wait_for_prompt()
            
            # Simple check - look for reasonable values
            if self._looks_like_board(output):
                self.board_address = addr
                print(f"✅ Found board at {addr}")
                return True
                
        return False
        
    def _looks_like_board(self, output):
        """Check if memory dump looks like a game board."""
        # Extract values
        values = re.findall(r'0x([0-9a-fA-F]+)', output)
        
        if len(values) < 16:
            return False
            
        # Convert to integers
        try:
            ints = [int(v, 16) for v in values[:16]]
            
            # Check if values are reasonable
            zeros = sum(1 for v in ints if v == 0)
            powers = sum(1 for v in ints if v > 0 and (v & (v-1)) == 0)
            
            return zeros > 0 and (zeros + powers) >= 16
        except:
            return False
            
    def enable_ai(self):
        """Enable AI control."""
        print("🤖 Enabling AI...")
        
        # Set breakpoint on input
        self._send_command("break wgetch")
        self._wait_for_prompt()
        
        # Set commands
        self._send_command("commands")
        self._send_command("silent")
        self._send_command("return 115")  # 's' key - always go down
        self._send_command("continue")
        self._send_command("end")
        self._wait_for_prompt()
        
        print("✅ AI enabled - will always press DOWN")
        
    def run(self):
        """Main control loop."""
        print("\n🎮 2048 AI Controller")
        print("=" * 40)
        
        self.start()
        
        print("\nWait for the board to appear, then press Enter...")
        input()
        
        self.interrupt_game()
        
        if self.find_board():
            self.enable_ai()
            
            # Continue game
            self._send_command("continue")
            
            print("\n✅ AI is now playing!")
            print("Press Ctrl+C to stop")
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Stopping...")
                self.gdb.terminate()
        else:
            print("❌ Could not find board")
            self.gdb.terminate()

if __name__ == "__main__":
    controller = External2048Controller()
    controller.run()
