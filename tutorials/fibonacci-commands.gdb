# GDB command file for fibonacci debugging

# Pretty printing
set print pretty on
set print array on
set pagination off

# Define a function to trace fibonacci calls
define trace_fib
    break fib_recursive
    commands
        silent
        printf "fib(%d) called\n", n
        continue
    end
end

# Define a function to examine the memo cache
define show_memo
    if memo_initialized
        printf "Memoization cache (first 20 entries):\n"
        set $i = 0
        while $i < 20
            if memo_cache[$i] != -1
                printf "  memo[%d] = %ld\n", $i, memo_cache[$i]
            end
            set $i = $i + 1
        end
    else
        printf "Memo cache not initialized\n"
    end
end

# Useful breakpoints
break main
break fib_buggy

# Run with argument
run 15

# At main breakpoint, examine initial state
print n
continue

# The program will run to completion
