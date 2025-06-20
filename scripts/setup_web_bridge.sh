#!/bin/sh
#!/bin/sh

echo "Setting up GDB Web Bridge..."

# Install Flask if needed
pip install flask requests

echo "Starting web bridge..."
echo "In another terminal, you can use:"
echo "  python3 claude_client.py"
echo ""

python3 gdb_web_bridge.py
