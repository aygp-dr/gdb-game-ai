# GDB Game AI - 2048 Analysis Framework

This project provides a framework for Claude Code to interact with games through GDB, starting with 2048.

## Quick Start

```bash
# Setup
./setup-claude-code.sh

# Analyze source
python3 src/python/analyze_2048_source.py

# Start interactive session
python3 claude_code_interface.py
```

## Project Structure

```
gdb-game-ai/
├── experiments/          # Experiment results
│   ├── 01-source-analysis/
│   ├── 02-memory-search/
│   └── 03-ai-testing/
├── src/
│   ├── python/          # Python tools
│   │   ├── analyze_2048_source.py
│   │   └── gdb_bridge.py
│   └── scheme/          # Guile Scheme GDB scripts
├── 2048-source/         # Source code for analysis
├── logs/                # GDB session logs
└── claude_code_interface.py  # Main interface
```

## For Claude Code

Use `claude_code_interface.py` as your main entry point:

```python
from claude_code_interface import ClaudeCodeInterface

# Create interface
interface = ClaudeCodeInterface()

# Follow the steps
summary = interface.analyze_source()
interface.start_game()
interface.find_board(hint_value=16)  # Use a value you see
board = interface.read_board()
interface.make_move("auto")
```

## Experiments

See `NEXT_STEPS.md` for experiment ideas and research questions.

## Contributing

This is designed for experimentation. Feel free to:
- Add new analysis tools
- Implement better AI strategies  
- Create new experiments
- Document findings

## Goal

Transform 2048 from a simple game into a deeply understood system where we can:
- Predict optimal moves
- Prove winning strategies
- Push scoring boundaries
- Learn about AI and reverse engineering
