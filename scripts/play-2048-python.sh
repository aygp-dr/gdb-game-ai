#!/bin/sh
#!/bin/sh
# Play 2048 with Python-based AI

echo "🎮 Starting 2048 with AI..."

# Create GDB init script
cat > /tmp/2048-python.gdb << 'EOF'
# Load Python AI
source 2048-ai.py

# Start the game
run

# Instructions
echo
echo "========================================="
echo "Once the game starts showing the board:"
echo "  1. Press Ctrl+C to interrupt"
echo "  2. Type: find-board"
echo "  3. Type: ai-2048"
echo "  4. Type: continue"
echo "========================================="
echo
EOF

# Run GDB
gdb -x /tmp/2048-python.gdb /usr/local/bin/2048
