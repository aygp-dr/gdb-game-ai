# Running 2048 with Screen for GDB Integration

This guide explains how to run the 2048 game in a screen session for easier monitoring and GDB debugging.

## Using the Helper Script

We've included a helper script that sets everything up for you:

```bash
# Run the helper script
./scripts/screen-run.sh
```

## Manual Setup

If you prefer to set things up manually:

```bash
# Start in screen with logging
screen -dmS game2048 -L -Logfile /tmp/game.log bash -c '
    exec 3>&1 4>&2
    /usr/local/bin/2048 2>&4 1>&3 | tee /tmp/2048_live.txt
'
```

## Working with the Game Session

Once the game is running in screen, you can:

### Monitor the Game

```bash
# Watch live output
tail -f /tmp/2048_live.txt

# Capture current screen to a file
screen -S game2048 -X hardcopy /tmp/screen.txt
cat /tmp/screen.txt
```

### Control the Game

```bash
# Send keystrokes to the game
screen -S game2048 -X stuff "s"  # sends 's' key (down)
screen -S game2048 -X stuff "w"  # sends 'w' key (up)
screen -S game2048 -X stuff "a"  # sends 'a' key (left)
screen -S game2048 -X stuff "d"  # sends 'd' key (right)
```

### Debug with GDB

```bash
# Attach GDB to the running process
gdb -p $(pgrep 2048)

# Load our scripts
source gdb/autoload.gdb

# Find the board and start the AI
find-board
ai-2048
```

### Attach to the Screen

```bash
# Attach to view the game directly
screen -x game2048

# Detach from screen without killing the game
# Press Ctrl+A followed by d
```

### Clean Up

```bash
# Kill the game and screen session
screen -S game2048 -X quit
```

## Advanced Usage

This setup provides several advantages:

1. The game runs in the background
2. You can monitor output without interfering with the game
3. You can send input programmatically
4. GDB can attach to the process
5. All output is logged for later analysis

This approach is particularly useful for automated testing and AI development.