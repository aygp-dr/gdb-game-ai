# GDB Web Bridge for Claude Code

This creates a web API that Claude Code can use to control GDB remotely.

## Setup

1. Install dependencies:
   ```bash
   pip install flask requests
   ```

2. Start the web bridge:
   ```bash
   python3 gdb_web_bridge.py
   ```

3. In Claude Code, use the client:
   ```python
   from claude_client import GDB2048Client
   
   client = GDB2048Client()
   client.start()
   client.run()
   # Wait a bit...
   client.interrupt()
   client.find_board()
   board = client.get_board()
   print(board)
   ```

## API Endpoints

- `POST /start` - Start GDB with 2048
- `POST /run` - Run the game  
- `POST /break` - Interrupt execution
- `POST /find-board` - Find game board in memory
- `GET /board` - Get current board state
- `POST /move` - Make a move (direction: up/down/left/right/auto)
- `POST /ai-enable` - Enable AI auto-play
- `POST /continue` - Continue execution

## Example Session

```python
# Full automated game
client = GDB2048Client()
client.play_game(moves=100)
```
