#!/usr/bin/env python3
"""
GDB Web Bridge - Allows Claude Code to interact with GDB via HTTP
"""

from flask import Flask, request, jsonify
import subprocess
import threading
import queue
import time
import re

app = Flask(__name__)

class GDBController:
    def __init__(self):
        self.process = None
        self.output_queue = queue.Queue()
        self.board_address = None
        
    def start(self, binary="/usr/local/bin/2048"):
        """Start GDB process."""
        self.process = subprocess.Popen(
            ["gdb", "-q", binary],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0
        )
        
        # Start output reader thread
        threading.Thread(target=self._read_output, daemon=True).start()
        
        # Load Python AI
        self.send_command("source 2048-ai.py")
        
        return {"status": "started", "pid": self.process.pid}
    
    def _read_output(self):
        """Read GDB output in background."""
        while self.process and self.process.poll() is None:
            line = self.process.stdout.readline()
            if line:
                self.output_queue.put(line.strip())
    
    def send_command(self, cmd):
        """Send command to GDB."""
        if not self.process:
            return {"error": "GDB not running"}
            
        self.process.stdin.write(cmd + "\n")
        self.process.stdin.flush()
        
        # Collect output
        output = []
        time.sleep(0.5)  # Give GDB time to respond
        
        while not self.output_queue.empty():
            try:
                line = self.output_queue.get_nowait()
                output.append(line)
            except queue.Empty:
                break
                
        return {"command": cmd, "output": output}
    
    def get_board(self):
        """Get current board state."""
        result = self.send_command("python game_board.read_board(); print(game_board.board)")
        
        # Parse board from output
        board_str = " ".join(result.get("output", []))
        
        # Extract numbers from the output
        numbers = re.findall(r'\d+', board_str)
        
        if len(numbers) >= 16:
            board = [int(n) for n in numbers[:16]]
            # Format as 4x4
            formatted = []
            for i in range(4):
                formatted.append(board[i*4:(i+1)*4])
            return {"board": formatted, "flat": board}
        
        return {"error": "Could not read board"}

# Global controller
gdb = GDBController()

# API Routes

@app.route('/start', methods=['POST'])
def start_gdb():
    """Start GDB with 2048."""
    return jsonify(gdb.start())

@app.route('/command', methods=['POST'])
def send_command():
    """Send command to GDB."""
    data = request.json
    cmd = data.get('command', '')
    return jsonify(gdb.send_command(cmd))

@app.route('/run', methods=['POST'])
def run_game():
    """Start the game."""
    return jsonify(gdb.send_command("run"))

@app.route('/break', methods=['POST'])
def break_execution():
    """Send interrupt signal."""
    if gdb.process:
        gdb.process.send_signal(subprocess.signal.SIGINT)
        time.sleep(0.5)
        return jsonify({"status": "interrupted"})
    return jsonify({"error": "GDB not running"})

@app.route('/find-board', methods=['POST'])
def find_board():
    """Find the game board."""
    return jsonify(gdb.send_command("find-board"))

@app.route('/board', methods=['GET'])
def get_board():
    """Get current board state."""
    return jsonify(gdb.get_board())

@app.route('/move', methods=['POST'])
def make_move():
    """Make a move."""
    data = request.json
    direction = data.get('direction', 'auto')
    
    # Map directions to keys
    moves = {
        'up': 'w',
        'down': 's',
        'left': 'a',
        'right': 'd',
        'auto': 'auto'
    }
    
    if direction == 'auto':
        # Use AI to decide
        gdb.send_command("python move = ai.choose_move()")
        return jsonify({"status": "AI choosing move"})
    else:
        key = moves.get(direction, 's')
        gdb.send_command(f"return (int){ord(key)}")
        return jsonify({"status": f"moved {direction}"})

@app.route('/ai-enable', methods=['POST'])
def enable_ai():
    """Enable AI auto-play."""
    return jsonify(gdb.send_command("ai-2048"))

@app.route('/continue', methods=['POST'])
def continue_execution():
    """Continue execution."""
    return jsonify(gdb.send_command("continue"))

@app.route('/status', methods=['GET'])
def get_status():
    """Get GDB status."""
    if gdb.process and gdb.process.poll() is None:
        return jsonify({"status": "running", "pid": gdb.process.pid})
    return jsonify({"status": "not running"})

if __name__ == '__main__':
    print("🌐 GDB Web Bridge")
    print("=" * 40)
    print("API Endpoints:")
    print("  POST /start        - Start GDB with 2048")
    print("  POST /run          - Run the game")
    print("  POST /break        - Interrupt execution")
    print("  POST /find-board   - Find game board")
    print("  GET  /board        - Get current board")
    print("  POST /move         - Make a move")
    print("  POST /ai-enable    - Enable AI")
    print("  POST /continue     - Continue execution")
    print("  GET  /status       - Get GDB status")
    print("\nStarting server on http://localhost:5000")
    
    app.run(debug=True, port=5000)
