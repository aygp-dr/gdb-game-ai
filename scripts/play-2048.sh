#!/bin/sh
#!/bin/sh
# Quick script to play 2048 with AI

cat > /tmp/2048-ai-init.gdb << 'EOF'
# Load Guile support
set guile print-stack full

# Load our AI
guile (load "src/scheme/2048-ai.scm")

# Instructions
printf "\n=== 2048 AI Controller ===\n"
printf "1. First, find the board address:\n"
printf "   - Let the game start\n"
printf "   - Use: find /w 0x400000, 0x500000, <unique-value>\n"
printf "   - Look for a 16-integer sequence that matches the board\n"
printf "2. Set the address: 2048-set-addr 0xADDRESS\n"
printf "3. Enable AI: 2048-auto\n"
printf "4. Continue playing: continue\n\n"

# Break at main to start
break main
run
EOF

gdb -x /tmp/2048-ai-init.gdb /usr/local/bin/2048
