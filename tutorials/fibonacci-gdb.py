#!/usr/bin/env python3
"""GDB Python script for analyzing fibonacci implementations"""

import gdb

class FibonacciAnalyzer(gdb.Command):
    """Analyze fibonacci execution patterns"""
    
    def __init__(self):
        super(FibonacciAnalyzer, self).__init__("analyze-fib", gdb.COMMAND_USER)
        self.call_counts = {}
        
    def invoke(self, arg, from_tty):
        # Set up breakpoint with callback
        bp = FibBreakpoint()
        
        # Run the program
        gdb.execute(f"run {arg}")
        
        # Print analysis
        print("\nCall frequency analysis:")
        for n, count in sorted(bp.call_counts.items()):
            print(f"  fib({n}) called {count} times")

class FibBreakpoint(gdb.Breakpoint):
    """Breakpoint that tracks fibonacci calls"""
    
    def __init__(self):
        super(FibBreakpoint, self).__init__("fib_recursive")
        self.call_counts = {}
        
    def stop(self):
        # Get the value of n
        n = int(gdb.parse_and_eval("n"))
        
        # Track calls
        self.call_counts[n] = self.call_counts.get(n, 0) + 1
        
        # Don't actually stop
        return False

class MemoWatcher(gdb.Command):
    """Watch memoization cache effectiveness"""
    
    def __init__(self):
        super(MemoWatcher, self).__init__("watch-memo", gdb.COMMAND_USER)
        
    def invoke(self, arg, from_tty):
        # Set watchpoint on memo statistics
        gdb.execute("watch memo_hits")
        gdb.execute("watch memo_misses")
        
        # Run program
        gdb.execute(f"run {arg}")

# Register commands
FibonacciAnalyzer()
MemoWatcher()

print("Fibonacci GDB analysis commands loaded:")
print("  analyze-fib N  - Analyze call patterns for fib(N)")
print("  watch-memo N   - Watch memoization effectiveness")
