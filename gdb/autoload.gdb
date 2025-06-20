# GDB Game AI - Autoload script
# This script loads all necessary GDB commands and functionality

# Banner
echo \n\033[1;36m GDB Game AI - 2048 Game Controller \033[0m\n
echo \033[1mA framework for analyzing and controlling games through GDB\033[0m
echo \033[90mhttps://github.com/aygp-dr/gdb-game-ai\033[0m\n

# Set better GDB defaults
set confirm off
set print elements 0
set pagination off

# Check if Python support is available
python
import sys
try:
    print("Python " + sys.version.split()[0] + " support available")
    python_available = True
except:
    python_available = False
end

# Load Python AI if Python is available
if $python_available
    echo \033[32m[✓] Loading Python AI support...\033[0m\n
    source ../src/python/ai/basic_ai.py
else
    echo \033[31m[✗] Python support not available, falling back to basic GDB scripts\033[0m\n
endif

# Load basic board detection
source find-board.gdb

# Check if Guile/Scheme support is available
python
try:
    import gdb
    result = gdb.execute("guile (display \"Scheme test\")", to_string=True)
    scheme_available = "Scheme test" in result
    print("Guile Scheme support: " + ("Available" if scheme_available else "Not available"))
except:
    scheme_available = False
end

# Load Scheme AI if available
if $scheme_available
    echo \033[32m[✓] Loading Scheme AI support...\033[0m\n
    source ../src/scheme/2048-ai.scm
else
    echo \033[90m[i] Guile Scheme not available, skipping Scheme AI\033[0m\n
endif

# Basic AI fallback
source simple-ai-fixed.gdb

# Usage information
echo \033[1mAvailable commands:\033[0m\n
echo \033[33mfind-board\033[0m - Find the 2048 board in memory
echo \033[33mset-board <addr>\033[0m - Manually set board address
echo \033[33mshow-board\033[0m - Display current board state
echo \033[33mai-2048\033[0m - Enable AI auto-play
echo \n\033[90mStart by running the game, then use find-board, then ai-2048\033[0m\n