#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Global variables for inspection
long recursive_calls = 0;
long memo_hits = 0;
long memo_misses = 0;

// Memoization cache
#define MAX_MEMO 100
long memo_cache[MAX_MEMO];
int memo_initialized = 0;

// Basic recursive Fibonacci
long fib_recursive(int n) {
    recursive_calls++;
    
    if (n <= 1) {
        return n;
    }
    
    return fib_recursive(n - 1) + fib_recursive(n - 2);
}

// Memoized Fibonacci
long fib_memoized(int n) {
    // Initialize cache on first call
    if (!memo_initialized) {
        memset(memo_cache, -1, sizeof(memo_cache));
        memo_initialized = 1;
    }
    
    if (n < 0 || n >= MAX_MEMO) {
        fprintf(stderr, "Error: n must be between 0 and %d\n", MAX_MEMO - 1);
        return -1;
    }
    
    if (n <= 1) {
        return n;
    }
    
    // Check cache
    if (memo_cache[n] != -1) {
        memo_hits++;
        return memo_cache[n];
    }
    
    // Calculate and cache
    memo_misses++;
    memo_cache[n] = fib_memoized(n - 1) + fib_memoized(n - 2);
    return memo_cache[n];
}

// Iterative Fibonacci for comparison
long fib_iterative(int n) {
    if (n <= 1) return n;
    
    long a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        long temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Helper function to measure time
double measure_time(long (*fib_func)(int), int n, long *result) {
    clock_t start = clock();
    *result = fib_func(n);
    clock_t end = clock();
    return ((double)(end - start)) / CLOCKS_PER_SEC;
}

// Function with a bug for debugging practice
long fib_buggy(int n) {
    // Bug: doesn't handle n=0 correctly
    if (n == 1) return 1;
    if (n == 2) return 1;
    return fib_buggy(n - 1) + fib_buggy(n - 2);
}

void print_statistics() {
    printf("\nStatistics:\n");
    printf("  Recursive calls: %ld\n", recursive_calls);
    printf("  Memo hits: %ld\n", memo_hits);
    printf("  Memo misses: %ld\n", memo_misses);
    if (memo_hits + memo_misses > 0) {
        printf("  Cache hit rate: %.2f%%\n", 
               (100.0 * memo_hits) / (memo_hits + memo_misses));
    }
}

void reset_statistics() {
    recursive_calls = 0;
    memo_hits = 0;
    memo_misses = 0;
}

int main(int argc, char *argv[]) {
    int n = 10;  // Default value
    
    if (argc > 1) {
        n = atoi(argv[1]);
        if (n < 0 || n > 45) {
            fprintf(stderr, "Please use n between 0 and 45\n");
            return 1;
        }
    }
    
    printf("Calculating Fibonacci(%d)\n", n);
    printf("==========================\n\n");
    
    long result;
    double time_taken;
    
    // Test recursive version
    reset_statistics();
    printf("Recursive implementation:\n");
    time_taken = measure_time(fib_recursive, n, &result);
    printf("  fib(%d) = %ld\n", n, result);
    printf("  Time: %.6f seconds\n", time_taken);
    printf("  Calls: %ld\n", recursive_calls);
    
    // Test memoized version
    reset_statistics();
    memo_initialized = 0;  // Reset memo cache
    printf("\nMemoized implementation:\n");
    time_taken = measure_time(fib_memoized, n, &result);
    printf("  fib(%d) = %ld\n", n, result);
    printf("  Time: %.6f seconds\n", time_taken);
    print_statistics();
    
    // Test iterative version
    printf("\nIterative implementation:\n");
    time_taken = measure_time(fib_iterative, n, &result);
    printf("  fib(%d) = %ld\n", n, result);
    printf("  Time: %.6f seconds\n", time_taken);
    
    // Demonstrate the buggy version (commented out to avoid crash)
    // printf("\nBuggy implementation:\n");
    // result = fib_buggy(n);  // This will crash for n=0!
    // printf("  fib(%d) = %ld\n", n, result);
    
    return 0;
}
