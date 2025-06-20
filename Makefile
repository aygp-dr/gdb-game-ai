# Makefile for 2048-cli with debug symbols for GDB
# Based on https://github.com/Tiehuis/2048-cli

# Variables
VERSION := v0.9.1
SOURCE_URL := https://codeload.github.com/Tiehuis/2048-cli/tar.gz/$(VERSION)
SOURCE_DIR := 2048-source
BUILD_DIR := $(SOURCE_DIR)/build
DOWNLOAD_FILE := /tmp/2048-cli.tar.gz

# Paper resources
PAPER_URL := https://theresamigler.com/wp-content/uploads/2020/03/2048.pdf
PAPER_FILE := docs/papers/2048.pdf
PAPER_DIR := docs/papers

# Compiler options
CC := gcc
CFLAGS := -g -O0 -Wall -Wextra # -g adds debug symbols, -O0 disables optimization
NCURSES_FLAGS := -lncurses

# Binary locations
LOCAL_BIN := ./bin/2048
SYSTEM_BIN := /usr/local/bin/2048

# Default target
all: download build

# Help
help:
	@echo "2048-cli Build Makefile with GDB Support"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Download and build 2048 with debug symbols"
	@echo "  download     - Download 2048 source code"
	@echo "  build        - Build 2048 with debug symbols"
	@echo "  install      - Install 2048 to /usr/local/bin (requires sudo)"
	@echo "  install-local - Install 2048 to ./bin directory"
	@echo "  clean        - Remove build files"
	@echo "  run          - Run 2048"
	@echo "  debug        - Run 2048 with GDB"
	@echo "  ai           - Run 2048 with GDB and Python AI"
	@echo "  paper        - Download the 2048 AI research paper"
	@echo ""
	@echo "Options:"
	@echo "  VERSION      - 2048-cli version to use (default: $(VERSION))"

# Download 2048 source code
download:
	@echo "Downloading 2048-cli source code..."
	@mkdir -p /tmp
	@wget -q $(SOURCE_URL) -O $(DOWNLOAD_FILE)
	@echo "Extracting source code..."
	@mkdir -p $(SOURCE_DIR)
	@tar -xzf $(DOWNLOAD_FILE) --strip-components=1 -C $(SOURCE_DIR)
	@echo "Source code downloaded to $(SOURCE_DIR)"

# Build 2048 with debug symbols
build: $(SOURCE_DIR)
	@echo "Building 2048 with debug symbols..."
	@mkdir -p $(BUILD_DIR)
	@cd $(SOURCE_DIR) && $(MAKE) CFLAGS="$(CFLAGS)" debug
	@mkdir -p bin
	@cp $(SOURCE_DIR)/2048 $(LOCAL_BIN)
	@echo "Build complete: $(LOCAL_BIN)"

# Install 2048 to /usr/local/bin
install: build
	@echo "Installing 2048 to $(SYSTEM_BIN)..."
	@sudo cp $(LOCAL_BIN) $(SYSTEM_BIN)
	@echo "Installation complete"

# Install 2048 locally
install-local: build
	@echo "Installing 2048 locally to $(LOCAL_BIN)..."
	@mkdir -p bin
	@cp $(SOURCE_DIR)/2048 $(LOCAL_BIN)
	@echo "Local installation complete"

# Clean build files
clean:
	@echo "Cleaning build files..."
	@cd $(SOURCE_DIR) && $(MAKE) clean
	@rm -f $(LOCAL_BIN)
	@echo "Clean complete"

# Run 2048
run: build
	@echo "Running 2048..."
	@$(LOCAL_BIN)

# Run 2048 with GDB
debug: build
	@echo "Running 2048 with GDB..."
	@gdb $(LOCAL_BIN)

# Run 2048 with GDB and Python AI
ai: build
	@echo "Running 2048 with GDB and Python AI..."
	@echo '# Load Python AI' > /tmp/2048-python.gdb
	@echo 'source src/python/ai/basic_ai.py' >> /tmp/2048-python.gdb
	@echo '' >> /tmp/2048-python.gdb
	@echo '# Start the game' >> /tmp/2048-python.gdb
	@echo 'run' >> /tmp/2048-python.gdb
	@echo '' >> /tmp/2048-python.gdb
	@echo '# Instructions' >> /tmp/2048-python.gdb
	@echo 'echo' >> /tmp/2048-python.gdb
	@echo 'echo "========================================="' >> /tmp/2048-python.gdb
	@echo 'echo "Once the game starts showing the board:"' >> /tmp/2048-python.gdb
	@echo 'echo "  1. Press Ctrl+C to interrupt"' >> /tmp/2048-python.gdb
	@echo 'echo "  2. Type: find-board"' >> /tmp/2048-python.gdb
	@echo 'echo "  3. Type: ai-2048"' >> /tmp/2048-python.gdb
	@echo 'echo "  4. Type: continue"' >> /tmp/2048-python.gdb
	@echo 'echo "========================================="' >> /tmp/2048-python.gdb
	@echo 'echo' >> /tmp/2048-python.gdb
	@gdb -x /tmp/2048-python.gdb $(LOCAL_BIN)

# Download the 2048 AI research paper
paper:
	@echo "Downloading 2048 AI research paper..."
	@mkdir -p $(PAPER_DIR)
	@wget -q $(PAPER_URL) -O $(PAPER_FILE)
	@echo "Paper downloaded to $(PAPER_FILE)"
	@echo ""
	@echo "This paper by Theresa Migler discusses various AI strategies for 2048."
	@echo "It's a great resource for understanding and implementing heuristics."
	@echo ""
	@echo "To read the paper: xdg-open $(PAPER_FILE) or open it with your PDF viewer"

# Handle source directory exists case
$(SOURCE_DIR):
	@echo "Source directory not found. Running download target..."
	@$(MAKE) download

.PHONY: all download build install install-local clean run debug ai help paper