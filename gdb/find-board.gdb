# GDB Game AI - Find Board Script
# Simple board detection for 2048

# Define the board detection command
define find-board
    echo Searching for 2048 board...\n
    
    # Try common memory patterns for 2048 board
    # First try: 0, 0, 0, 2 (common starting pattern)
    find /w 0x400000, 0x700000, 0, 0, 0, 2
    
    # Remember to verify:
    # - Board should be 16 integers (4x4)
    # - Values should be 0 or powers of 2
    # - When found, use "x/16wx ADDRESS" to view
    
    echo \nIf a match is found, use:\n
    echo "x/16wx ADDRESS" to view potential board\n
    echo "set $board_addr = ADDRESS" to save the address\n
end

# Define a command to display board given address
define show-board
    if $argc == 0
        if $board_addr
            set $addr = $board_addr
        else
            echo Error: No board address set. Use "set $board_addr = ADDRESS" first.\n
            help show-board
            quit
        end
    else
        set $addr = $arg0
    end
    
    echo \n2048 Game Board:\n
    echo +-----------------------+\n
    
    set $row = 0
    while $row < 4
        set $col = 0
        printf "| "
        while $col < 4
            set $cell = *((int*)($addr + (($row * 4 + $col) * 4)))
            if $cell == 0
                printf "    . | "
            else
                printf "%5d | ", $cell
            end
            set $col = $col + 1
        end
        echo \n+-----------------------+\n
        set $row = $row + 1
    end
end

# Help message
document find-board
Find the 2048 game board in memory.
This command searches for common patterns in the expected memory range.
When a potential match is found, examine it with "x/16wx ADDRESS"
and if it looks like a valid board, save with "set $board_addr = ADDRESS"
end

document show-board
Usage: show-board [address]
Display the 2048 game board in a readable format.
If address is omitted, uses the saved $board_addr.
end