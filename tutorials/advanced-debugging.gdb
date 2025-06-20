# Advanced GDB session for fibonacci

# TUI mode for source viewing
# tui enable
# layout src

# Set up conditional breakpoint
break fib_recursive if n == 0 || n == 1
commands
    printf "Base case: fib(%d) = %d\n", n, n
    continue
end

# Watch global variables
display recursive_calls
display memo_hits
display memo_misses

# Set up catchpoint for the buggy function
catch assert

# Memory examination function
define examine_memo
    print "Examining memoization cache:"
    # Show first 20 entries
    print memo_cache[0]@20
    
    # Count non-empty entries
    set $i = 0
    set $count = 0
    while $i < 100
        if memo_cache[$i] != -1
            set $count = $count + 1
        end
        set $i = $i + 1
    end
    printf "Cache entries used: %d / 100\n", $count
end

# Performance analysis function
define perf_compare
    set $n = $arg0
    
    # Test recursive
    set recursive_calls = 0
    call fib_recursive($n)
    printf "Recursive calls for fib(%d): %ld\n", $n, recursive_calls
    
    # Test memoized
    set memo_hits = 0
    set memo_misses = 0
    call fib_memoized($n)
    printf "Memoized - hits: %ld, misses: %ld\n", memo_hits, memo_misses
end

# Stepping through with auto-display
define smart_step
    while 1
        step
        if $rip == fib_recursive || $rip == fib_memoized
            backtrace 3
            info locals
        end
    end
end
