#!/bin/bash
#!/bin/bash
# Performance analysis with GDB

echo "=== Performance Analysis ==="

for n in 10 20 30 35; do
    echo -e "\nAnalyzing fib($n):"
    gdb -batch -quiet \
        -ex "file fibonacci" \
        -ex "break fib_recursive" \
        -ex "ignore 1 1000000" \
        -ex "run $n" \
        -ex "info breakpoints" \
        ./fibonacci 2>&1 | grep "hit [0-9]" | awk '{print "  Recursive calls:", $NF}'
done
