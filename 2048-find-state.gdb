# Find the game board in memory
break main
run

# When at main, let's search for patterns
# The board you showed has: empty, 2, 2, 8, 16
# In memory, empty is likely 0, and values are powers of 2

# Let's search for your exact board pattern
# Row 1: 0, 0, 0, 2
# Row 2: 2, 0, 0, 2
# Row 3: 0, 0, 0, 8
# Row 4: 0, 2, 16, 2

# Continue to the game screen
continue

# Now let's find where these values are stored
# Search for the sequence 0,0,0,2 (first row)
find /w 0x400000, 0x500000, 0, 0, 0, 2

# Or search for the unique value 16
find /w 0x400000, 0x500000, 16
