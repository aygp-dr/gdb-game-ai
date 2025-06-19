#!/usr/bin/env python3
"""
Claude Code Interface - High-level interface for Claude Code to interact with 2048 via GDB.
"""

import json
from pathlib import Path
from src.python.gdb_bridge import GDBBridge
from src.python.analyze_2048_source import SourceAnalyzer

class ClaudeCodeInterface:
    """
    High-level interface designed for Claude Code interaction.
    Provides simple methods that Claude Code can call to explore and control the game.
    """
    
    def __init__(self):
        self.gdb = None
        self.board_address = None
        self.source_analysis = None
        
    def analyze_source(self):
        """
        Step 1: Analyze the source code to understand the game structure.
        Returns a summary that Claude Code can use.
        """
        print("📚 Analyzing 2048 source code...")
        analyzer = SourceAnalyzer()
        self.source_analysis = analyzer.analyze_all()
        
        # Create Claude-friendly summary
        summary = {
            "likely_board_structure": "int board[4][4] or similar",
            "board_size_bytes": 64,
            "hints_for_finding_board": self.source_analysis["memory_hints"],
            "key_functions": list(self.source_analysis["functions"].keys()),
            "next_steps": [
                "Use find_board() to locate the board in memory",
                "Once found, use read_board() to get current state",
                "Use make_move() to have the AI play"
            ]
        }
        
        return summary
    
    def start_game(self):
        """
        Step 2: Start the game under GDB control.
        """
        print("🎮 Starting 2048 under GDB control...")
        self.gdb = GDBBridge()
        self.gdb.start()
        
        # Run the game
        self.gdb.send_command("run")
        
        return "Game started. Use find_board() next."
    
    def find_board(self, hint_value=None):
        """
        Step 3: Find the game board in memory.
        
        Args:
            hint_value: A value you see on the board (like 16 or 32) to help narrow search
        """
        print(f"🔍 Searching for game board{' with hint: ' + str(hint_value) if hint_value else ''}...")
        
        if not self.gdb:
            return "Error: Start game first with start_game()"
        
        # Try different search strategies
        candidates = []
        
        if hint_value:
            # Search for the specific value
            addrs = self.gdb.find_board_pattern([hint_value])
            for addr in addrs:
                # Check addresses around it
                for offset in range(-60, 4, 4):  # Check up to 15 integers before
                    check_addr = hex(int(addr, 16) + offset)
                    if self._check_if_board(check_addr):
                        candidates.append(check_addr)
        
        # Also try common patterns
        patterns = [
            [0, 0, 0, 2],  # Common starting pattern
            [2, 0, 0, 2],
            [0, 2, 4, 0]
        ]
        
        for pattern in patterns:
            addrs = self.gdb.find_board_pattern(pattern)
            for addr in addrs:
                if self._check_if_board(addr):
                    candidates.append(addr)
        
        if candidates:
            self.board_address = candidates[0]
            return {
                "found": True,
                "address": self.board_address,
                "candidates": candidates[:5],
                "next_step": "Use read_board() to see the current state"
            }
        else:
            return {
                "found": False,
                "hint": "Try providing a unique value from the board as hint_value",
                "example": "find_board(hint_value=16)"
            }
    
    def _check_if_board(self, addr):
        """Check if an address contains a valid board."""
        try:
            values = self.gdb.examine_memory(addr, 16)
            return self.gdb.verify_board_address(addr)
        except:
            return False
    
    def read_board(self):
        """
        Step 4: Read the current board state.
        """
        if not self.board_address:
            return "Error: Find board first with find_board()"
        
        values = self.gdb.examine_memory(self.board_address, 16)
        
        # Format as 4x4 grid
        board = []
        for i in range(4):
            row = values[i*4:(i+1)*4]
            board.append(row)
        
        # Pretty print
        print("\nCurrent Board:")
        for row in board:
            print(" ".join(f"{v:4d}" if v > 0 else "   ." for v in row))
        
        return {
            "board": board,
            "flat": values,
            "empty_cells": sum(1 for v in values if v == 0),
            "max_tile": max(values) if values else 0
        }
    
    def make_move(self, direction="auto"):
        """
        Step 5: Make a move.
        
        Args:
            direction: "up", "down", "left", "right", or "auto" for AI choice
        """
        if not self.board_address:
            return "Error: Find board first with find_board()"
        
        # Read current board
        board_state = self.read_board()
        
        if direction == "auto":
            # Simple AI strategy
            direction = self._choose_best_move(board_state["flat"])
        
        # Map direction to key
        key_map = {
            "up": "w",
            "down": "s", 
            "left": "a",
            "right": "d"
        }
        
        key = key_map.get(direction, "s")
        
        # Inject the key at next input
        print(f"🎯 Making move: {direction} (key: {key})")
        
        # This is simplified - in practice we'd set up proper breakpoint handling
        self.gdb.send_command(f"call (void)printf(\"\\n\")")  # Trigger refresh
        
        return f"Move {direction} queued. Board should update soon."
    
    def _choose_best_move(self, board):
        """Simple AI to choose move."""
        # Very basic: prefer down and right to keep tiles in corner
        # In practice, would implement minimax or expectimax
        return "down"  # Simplified
    
    def run_experiment(self, name="auto_play", moves=10):
        """
        Run an experiment.
        
        Args:
            name: Experiment name
            moves: Number of moves to make
        """
        results = {
            "experiment": name,
            "moves": [],
            "scores": []
        }
        
        for i in range(moves):
            board_state = self.read_board()
            results["moves"].append(board_state)
            
            move = self.make_move("auto")
            print(f"Move {i+1}/{moves}: {move}")
            
            # Wait a bit for game to update
            import time
            time.sleep(0.5)
        
        # Save results
        exp_dir = Path(f"experiments/03-ai-testing/{name}")
        exp_dir.mkdir(parents=True, exist_ok=True)
        
        with open(exp_dir / "results.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        return f"Experiment '{name}' complete. Results saved."

# Quick start functions for Claude Code
def quick_start():
    """Quick start for Claude Code."""
    interface = ClaudeCodeInterface()
    
    print("🚀 2048 AI Quick Start")
    print("=" * 50)
    print("\n1️⃣ First, analyze the source:")
    print("   summary = interface.analyze_source()")
    print("\n2️⃣ Start the game:")
    print("   interface.start_game()")
    print("\n3️⃣ Find the board (look at the game and pick a unique number):")
    print("   interface.find_board(hint_value=16)")
    print("\n4️⃣ Read the board:")
    print("   interface.read_board()")
    print("\n5️⃣ Make moves:")
    print("   interface.make_move('down')")
    print("   interface.make_move('auto')  # AI chooses")
    print("\n6️⃣ Run experiment:")
    print("   interface.run_experiment('test', moves=20)")
    
    return interface

if __name__ == "__main__":
    # Create an instance for Claude Code to use
    interface = quick_start()
