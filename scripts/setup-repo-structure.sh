#!/bin/bash
# Create complete repository structure

# Create directories
mkdir -p src/{python,scheme,c,gdb}
mkdir -p experiments/{01-source-analysis,02-memory-search,03-ai-testing}
mkdir -p docs/{api,tutorials,research}
mkdir -p tests/{unit,integration}
mkdir -p games/{2048,umoria,nethack}
mkdir -p logs
mkdir -p tools
mkdir -p web/{static,templates}

# Move existing files to proper locations
mv 2048-ai.py src/python/
mv *.gdb src/gdb/
mv simple-ai*.gdb src/gdb/

# Create main entry points
cat > run.py << 'EOF'
#!/usr/bin/env python3
"""Main entry point for GDB Game AI"""

import sys
from src.python.gdb_bridge import GDBBridge
from claude_code_interface import ClaudeCodeInterface

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        from gdb_web_bridge import app
        app.run(debug=True)
    else:
        # Interactive mode
        interface = ClaudeCodeInterface()
        print("GDB Game AI Interface")
        print("Use: interface.start_game(), interface.find_board(), etc.")
        return interface

if __name__ == "__main__":
    main()
EOF

# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# Compiled files
*.o
*.so
*.pyc
__pycache__/
build/

# GDB files
.gdb_history
core
*.core

# Game binaries
fibonacci
2048
umoria

# Logs
logs/*.log
*.log

# Experiments output
experiments/*/results.json
experiments/*/output/

# IDE
.vscode/
.idea/
*.swp
*~

# OS
.DS_Store
Thumbs.db

# Python
venv/
.env
*.egg-info/
dist/
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
flask>=2.0.0
requests>=2.25.0
pytest>=6.0.0
psutil>=5.8.0
EOF

# Create pytest configuration
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
EOF

# Make scripts executable
chmod +x setup-claude-code.sh
chmod +x setup_web_bridge.sh
chmod +x test-2048.sh
chmod +x run.py

echo "Repository structure created!"
