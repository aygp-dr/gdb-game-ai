#!/usr/bin/env python3
"""
GDB Game AI - Main entry point
A framework for analyzing and controlling games through GDB
"""

import argparse
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point for GDB Game AI"""
    parser = argparse.ArgumentParser(description='GDB Game AI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Python AI command
    python_parser = subparsers.add_parser('python', help='Run with Python AI')
    python_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Scheme AI command
    scheme_parser = subparsers.add_parser('scheme', help='Run with Scheme AI')
    scheme_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Web interface command
    web_parser = subparsers.add_parser('web', help='Start web interface')
    web_parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'python':
        print("Starting 2048 with Python AI...")
        from python.claude_code_interface import main as python_main
        python_main(debug=args.debug)
    elif args.command == 'scheme':
        print("Starting 2048 with Scheme AI...")
        # Call the shell script that runs GDB with Scheme script
        os.system(f"bash {os.path.join(os.path.dirname(__file__), 'scripts/play-2048.sh')}")
    elif args.command == 'web':
        print(f"Starting web interface on port {args.port}...")
        from python.web.bridge import app
        app.run(host='0.0.0.0', port=args.port)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()