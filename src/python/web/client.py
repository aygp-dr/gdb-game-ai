#!/usr/bin/env python3
"""
Client for Claude Code to interact with GDB Web Bridge
"""

import requests
import json
import time

class GDB2048Client:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        
    def start(self):
        """Start GDB with 2048."""
        r = requests.post(f"{self.base_url}/start")
        return r.json()
    
    def run(self):
        """Run the game."""
        r = requests.post(f"{self.base_url}/run")
        return r.json()
    
    def interrupt(self):
        """Interrupt the game."""
        r = requests.post(f"{self.base_url}/break")
        return r.json()
    
    def find_board(self):
        """Find the board in memory."""
        r = requests.post(f"{self.base_url}/find-board")
        return r.json()
    
    def get_board(self):
        """Get current board state."""
        r = requests.get(f"{self.base_url}/board")
        return r.json()
    
    def move(self, direction="auto"):
        """Make a move."""
        r = requests.post(f"{self.base_url}/move", 
                         json={"direction": direction})
        return r.json()
    
    def enable_ai(self):
        """Enable AI auto-play."""
        r = requests.post(f"{self.base_url}/ai-enable")
        return r.json()
    
    def continue_execution(self):
        """Continue game execution."""
        r = requests.post(f"{self.base_url}/continue")
        return r.json()
    
    def play_game(self, moves=50):
        """Play a full game with AI."""
        print("🎮 Starting 2048 AI Game")
        
        # Start GDB
        print("Starting GDB...")
        self.start()
        time.sleep(1)
        
        # Run game
        print("Running game...")
        self.run()
        time.sleep(2)
        
        # Find board
        print("Finding board...")
        self.interrupt()
        time.sleep(0.5)
        self.find_board()
        
        # Enable AI
        print("Enabling AI...")
        self.enable_ai()
        
        # Continue and let AI play
        print("AI is playing...")
        self.continue_execution()
        
        # Monitor progress
        for i in range(moves):
            time.sleep(1)
            try:
                board = self.get_board()
                if "board" in board:
                    print(f"\nMove {i+1}:")
                    self.print_board(board["board"])
            except:
                pass
    
    def print_board(self, board):
        """Pretty print the board."""
        print("  " + "-" * 25)
        for row in board:
            line = "  |"
            for val in row:
                if val == 0:
                    line += "     |"
                else:
                    line += f"{val:5d}|"
            print(line)
        print("  " + "-" * 25)

# Example usage for Claude Code
if __name__ == "__main__":
    client = GDB2048Client()
    
    print("Claude Code can use this client:")
    print("```python")
    print("client = GDB2048Client()")
    print("client.start()")
    print("client.run()")
    print("# ... wait for board to appear ...")
    print("client.interrupt()")
    print("client.find_board()")
    print("board = client.get_board()")
    print("client.move('down')")
    print("```")
    
    # Or play automatically
    # client.play_game()
