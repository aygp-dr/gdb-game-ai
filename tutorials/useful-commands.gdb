# Print array nicely
set print array on
set print pretty on

# Print first 10 fibonacci numbers in cache
print memo_cache[0]@10

# Call function from GDB
print fib_iterative(20)

# Conditional breakpoint
break fib_recursive if n > 30

# Breakpoint with command
break fib_memoized
commands
    silent
    printf "Memo: fib(%d), hits=%ld, misses=%ld\n", n, memo_hits, memo_misses
    continue
end

# Watchpoint
watch recursive_calls

# Catch specific conditions
catch throw
catch assert

# Save breakpoints
save breakpoints fibonacci-breakpoints.gdb

# Load saved breakpoints
source fibonacci-breakpoints.gdb
