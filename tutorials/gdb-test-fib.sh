#!/usr/bin/env bash
#!/usr/bin/env bash
# Automated GDB testing script

echo "=== GDB Fibonacci Testing ==="

# Test 1: Count recursive calls
echo -e "\n1. Counting recursive calls for fib(10):"
gdb -batch -quiet \
    -ex "break fib_recursive" \
    -ex "commands" \
    -ex "silent" \
    -ex "continue" \
    -ex "end" \
    -ex "run 10" \
    -ex "print recursive_calls" \
    ./fibonacci 2>/dev/null | grep "recursive_calls"

# Test 2: Examine memoization cache
echo -e "\n2. Examining memoization cache after fib(10):"
gdb -batch -quiet \
    -ex "break print_statistics" \
    -ex "run 10" \
    -ex "print memo_cache[0]@11" \
    -ex "continue" \
    ./fibonacci 2>/dev/null | grep -A11 "memo_cache"

# Test 3: Performance comparison
echo -e "\n3. Breakpoint hit count comparison:"
gdb -batch -quiet \
    -ex "break fib_recursive" \
    -ex "ignore 1 1000000" \
    -ex "run 20" \
    -ex "info breakpoints" \
    ./fibonacci 2>/dev/null | grep "breakpoint.*hit"
