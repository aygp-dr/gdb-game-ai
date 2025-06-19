#!/usr/bin/env python3
"""
2048 AI for GDB - Works with Python support (no Guile needed)
"""

import gdb
import random

class GameBoard:
    """Represents the 2048 game board."""
    
    def __init__(self):
        self.address = None
        self.board = None
        
    def find_board(self):
        """Try to locate the game board in memory."""
        print("🔍 Searching for game board...")
        
        # Common patterns to search for
        patterns = [
            [0, 0, 0, 2],
            [2, 0, 0, 0],
            [0, 2, 0, 0],
            [2, 2, 0, 0]
        ]
        
        # Search in likely memory ranges
        for pattern in patterns:
            cmd = f"find /w 0x400000, 0x700000, {', '.join(map(str, pattern))}"
            try:
                results = gdb.execute(cmd, to_string=True)
                
                for line in results.split('\n'):
                    if '0x' in line:
                        addr = int(line.split()[0], 16)
                        # Check if this could be the start of a board
                        if self._verify_board(addr):
                            self.address = addr
                            print(f"✅ Found board at {hex(addr)}")
                            return True
            except:
                pass
                
        return False
    
    def _verify_board(self, addr):
        """Verify if address contains a valid game board."""
        try:
            # Read 16 integers
            values = []
            for i in range(16):
                val = self._read_int(addr + i * 4)
                values.append(val)
            
            # Check if it looks like a game board
            # All values should be 0 or powers of 2
            for val in values:
                if val < 0 or val > 65536:  # Unreasonable values
                    return False
                if val != 0 and (val & (val - 1)) != 0:  # Not power of 2
                    return False
            
            # Should have some empty cells and some tiles
            zeros = sum(1 for v in values if v == 0)
            if zeros == 0 or zeros == 16:
                return False
                
            self.board = values
            return True
            
        except:
            return False
    
    def _read_int(self, addr):
        """Read a 32-bit integer from memory."""
        result = gdb.execute(f"x/wx {hex(addr)}", to_string=True)
        # Parse the hex value from output
        parts = result.split()
        for part in parts:
            if part.startswith('0x'):
                return int(part, 16)
        return 0
    
    def read_board(self):
        """Read current board state."""
        if not self.address:
            return None
            
        board = []
        for i in range(16):
            val = self._read_int(self.address + i * 4)
            board.append(val)
        
        self.board = board
        return board
    
    def display(self):
        """Display the board."""
        if not self.board:
            print("No board data")
            return
            
        print("\n🎮 Current Board:")
        print("  " + "-" * 25)
        for row in range(4):
            line = "  |"
            for col in range(4):
                val = self.board[row * 4 + col]
                if val == 0:
                    line += "     |"
                else:
                    line += f"{val:5d}|"
            print(line)
        print("  " + "-" * 25)

class AI2048:
    """Simple AI for 2048."""
    
    def __init__(self, board):
        self.board = board
        
    def choose_move(self):
        """Choose the best move using simple strategy."""
        if not self.board.board:
            return ord('s')  # Default down
        
        # Check which moves are possible
        moves = {
            'down': ord('s'),
            'right': ord('d'),
            'left': ord('a'),
            'up': ord('w')
        }
        
        # Simple strategy: prefer down > right > left > up
        for direction in ['down', 'right', 'left', 'up']:
            if self._can_move(direction):
                print(f"🤖 AI chooses: {direction}")
                return moves[direction]
        
        return ord('q')  # No moves possible
    
    def _can_move(self, direction):
        """Check if a move is possible."""
        b = self.board.board
        
        if direction == 'down':
            for col in range(4):
                for row in range(3):
                    curr = b[row * 4 + col]
                    below = b[(row + 1) * 4 + col]
                    if curr != 0 and (below == 0 or below == curr):
                        return True
                        
        elif direction == 'up':
            for col in range(4):
                for row in range(1, 4):
                    curr = b[row * 4 + col]
                    above = b[(row - 1) * 4 + col]
                    if curr != 0 and (above == 0 or above == curr):
                        return True
                        
        elif direction == 'left':
            for row in range(4):
                for col in range(1, 4):
                    curr = b[row * 4 + col]
                    left = b[row * 4 + (col - 1)]
                    if curr != 0 and (left == 0 or left == curr):
                        return True
                        
        elif direction == 'right':
            for row in range(4):
                for col in range(3):
                    curr = b[row * 4 + col]
                    right = b[row * 4 + (col + 1)]
                    if curr != 0 and (right == 0 or right == curr):
                        return True
        
        return False

# Global instances
game_board = GameBoard()
ai = AI2048(game_board)

class AICommand(gdb.Command):
    """GDB command to enable AI play."""
    
    def __init__(self):
        super(AICommand, self).__init__("ai-2048", gdb.COMMAND_USER)
        
    def invoke(self, arg, from_tty):
        print("🎮 2048 AI Controller")
        print("=" * 40)
        
        # Try to find the board
        if not game_board.address:
            if not game_board.find_board():
                print("❌ Could not find board automatically.")
                print("Try:")
                print("  1. Let the game run first")
                print("  2. Use 'find-board' command")
                print("  3. Set manually with 'set-board 0xADDRESS'")
                return
        
        # Set up breakpoint
        gdb.execute("break wgetch")
        
        # Define breakpoint commands
        bp_commands = """commands
silent
python
game_board.read_board()
game_board.display()
move = ai.choose_move()
gdb.execute(f"return {move}")
end
end"""
        
        for line in bp_commands.split('\n'):
            gdb.execute(line)
        
        print("✅ AI enabled! Continue to start playing.")

class FindBoardCommand(gdb.Command):
    """Find the game board."""
    
    def __init__(self):
        super(FindBoardCommand, self).__init__("find-board", gdb.COMMAND_USER)
        
    def invoke(self, arg, from_tty):
        if game_board.find_board():
            game_board.read_board()
            game_board.display()
        else:
            print("Could not find board. Make sure game is running.")

class SetBoardCommand(gdb.Command):
    """Manually set board address."""
    
    def __init__(self):
        super(SetBoardCommand, self).__init__("set-board", gdb.COMMAND_USER)
        
    def invoke(self, arg, from_tty):
        try:
            addr = int(arg, 16) if arg.startswith('0x') else int(arg)
            game_board.address = addr
            print(f"Board address set to {hex(addr)}")
            game_board.read_board()
            game_board.display()
        except:
            print("Usage: set-board 0xADDRESS")

class ShowBoardCommand(gdb.Command):
    """Show current board."""
    
    def __init__(self):
        super(ShowBoardCommand, self).__init__("show-board", gdb.COMMAND_USER)
        
    def invoke(self, arg, from_tty):
        if game_board.address:
            game_board.read_board()
            game_board.display()
        else:
            print("Board not found. Use 'find-board' first.")

# Register commands
AICommand()
FindBoardCommand()
SetBoardCommand()
ShowBoardCommand()

print("🎮 2048 AI loaded! Commands:")
print("  ai-2048     - Enable AI auto-play")
print("  find-board  - Search for game board")
print("  show-board  - Display current board")
print("  set-board   - Manually set board address")
