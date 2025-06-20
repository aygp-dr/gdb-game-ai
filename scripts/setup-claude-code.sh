#!/bin/sh
#!/bin/sh
# Setup for Claude Code integration with GDB

echo "Setting up Claude Code GDB integration..."

# Create directory structure
mkdir -p experiments/{01-source-analysis,02-memory-search,03-ai-testing}
mkdir -p src/{python,scheme,analysis}
mkdir -p logs
mkdir -p tools

# Download 2048 source for analysis
echo "Downloading 2048-cli source..."
cd /tmp
wget https://codeload.github.com/Tiehuis/2048-cli/tar.gz/v0.9.1 -O 2048-cli.tar.gz
tar -xzf 2048-cli.tar.gz
cd -
cp -r /tmp/2048-cli-0.9.1 ./2048-source

echo "Setup complete!"
