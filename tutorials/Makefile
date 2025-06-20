# Makefile for Fibonacci GDB Tutorial

CC = gcc
CFLAGS = -g3 -O0 -Wall -Wextra -fno-omit-frame-pointer
TARGET = fibonacci

.PHONY: all clean run debug

all: $(TARGET)

$(TARGET): fibonacci.c
	$(CC) $(CFLAGS) -o $@ $<

run: $(TARGET)
	./$(TARGET) 10

# Various GDB debugging targets
debug: $(TARGET)
	gdb ./$(TARGET)

debug-batch: $(TARGET)
	gdb -batch -ex "break fib_recursive" -ex "run 5" -ex "bt" -ex "info locals" ./$(TARGET)

debug-mi: $(TARGET)
	gdb -i=mi ./$(TARGET)

clean:
	rm -f $(TARGET) core *.o

# Generate assembly for inspection
asm: fibonacci.c
	$(CC) $(CFLAGS) -S -fverbose-asm -o fibonacci.s fibonacci.c
