#!/bin/bash
# Run 2048 in a screen session with logging for easy monitoring and GDB debugging

# Start in screen with logging
screen -dmS game2048 -L -Logfile /tmp/game.log bash -c '
    exec 3>&1 4>&2
    /usr/local/bin/2048 2>&4 1>&3 | tee /tmp/2048_live.txt
'

echo "Game started in screen session 'game2048'"
echo ""
echo "Available commands:"
echo "  * Watch live output:      tail -f /tmp/2048_live.txt"
echo "  * Capture current screen: screen -S game2048 -X hardcopy /tmp/screen.txt"
echo "  * Send keystrokes:        screen -S game2048 -X stuff \"s\"  # sends 's' key"
echo "  * Attach GDB:             gdb -p \$(pgrep 2048)"
echo "  * Attach to screen:       screen -x game2048"
echo "  * Kill the game:          screen -S game2048 -X quit"
echo ""
echo "PID of 2048: \$(pgrep 2048)"