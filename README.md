# GDB Game AI

![Project Status: In Progress](https://img.shields.io/badge/Project%20Status-In%20Progress-yellow)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)
![GDB Required](https://img.shields.io/badge/GDB-Required-red)

A project for controlling and playing games using GDB as an interface, with AI integration for automated gameplay.

## Overview

This project leverages GDB (GNU Debugger) as a powerful interface to control and automate gameplay. By attaching GDB to running game processes, we can:

1. Analyze game memory structures
2. Read and manipulate game state
3. Inject inputs to control gameplay
4. Implement AI strategies to play games automatically

The initial focus is on the game 2048, with plans to expand to other games.

## Features

- Memory scanning to locate game board state
- GDB Python and Guile Scheme extensions for game control
- AI strategies from simple heuristics to advanced algorithms
- Web bridge for remote control and visualization
- Framework for experimentation and strategy comparison

## Getting Started

### Prerequisites

- GDB with Python and/or Guile support
- Python 3.6+
- 2048 game installed (typically available in package managers)

### Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/aygp-dr/gdb-game-ai.git
cd gdb-game-ai
./setup-repo-structure.sh
```

### Quick Start

To play 2048 with the AI using Python:

```bash
cd gdb-game-ai
./setup-claude-code.sh
python3 claude_code_interface.py
```

For Scheme-based approach:

```bash
./play-2048.sh
```

## Project Structure

```
gdb-game-ai/
   gdb-game-ai/              # Main implementation directory
      2048-ai.py            # Python-based AI for 2048
      claude_code_interface.py # Interface for Claude integration
      gdb_web_bridge.py     # Web API for remote control
      src/                  # Source code
          python/           # Python tools
              analyze_2048_source.py
              gdb_bridge.py
   src/                      # Alternative implementations
      scheme/               # Guile Scheme GDB scripts
          2048-ai.scm       # Scheme-based AI for 2048
          simple-2048.scm
   tutorials/                # GDB learning resources
      fibonacci.c           # Example C program for tutorials
      fibonacci-gdb.py      # Example GDB Python script
      useful-commands.gdb   # Useful GDB commands reference
   play-2048.sh              # Script to start 2048 with GDB+Scheme AI
   simple-ai.gdb             # Simple GDB script for basic AI
```

## AI Strategies

The project implements various AI strategies for playing 2048:

1. **Simple Priority Strategy**: Prefers moves in order: Down > Right > Left > Up
2. **Corner Strategy**: Keeps highest tile in a corner and builds a gradient
3. **Expectimax**: Looks ahead several moves considering random tile spawns
4. **Machine Learning**: Training models on successful game data (planned)

## GDB Integration

The project uses GDB in several innovative ways:

- **Memory Analysis**: Finding game state in process memory
- **Input Injection**: Simulating keyboard input through breakpoints
- **Game State Tracking**: Reading and validating board state
- **Automated Control**: Full automation through carefully placed breakpoints

## Web Bridge

A web API is provided to control the GDB session remotely:

```bash
python3 gdb_web_bridge.py
```

This allows programmatic control through HTTP requests or via the provided client:

```python
from claude_client import GDB2048Client
client = GDB2048Client()
client.start()
client.find_board()
client.play_game(moves=100)
```

## Development Roadmap

See [NEXT_STEPS.md](gdb-game-ai/NEXT_STEPS.md) for detailed development plans, including:

1. Board discovery improvements
2. Advanced AI strategies
3. Performance optimization
4. Extension to other games
5. Visualization and analysis tools

## Contributing

Contributions are welcome! This project is designed for experimentation and learning. Feel free to:

- Add new analysis tools
- Implement better AI strategies
- Create new experiments
- Document findings

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Developer Notes

- **Project Status**: This project is in active development. APIs and interfaces may change.
- **GDB Version**: Tested with GDB 10.1+ on Linux systems. Your mileage may vary with other versions.
- **Security**: Be cautious when running GDB scripts that interact with system memory. Always review scripts before execution.
- **Dependencies**: No external Python packages required for core functionality. Web bridge requires Flask.
- **Debugging Tips**: See the `tutorials` directory for GDB usage examples and tips.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- The 2048 game creators for making a great testbed for AI
- GDB developers for their powerful debugging interface
- Contributors to the Python and Scheme GDB extensions