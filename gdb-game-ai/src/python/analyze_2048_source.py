#!/usr/bin/env python3
"""
Analyze 2048-cli source code to understand memory layout.
This helps Claude Code understand the game structure.
"""

import os
import re
import json
from pathlib import Path

class SourceAnalyzer:
    def __init__(self, source_dir="2048-source"):
        self.source_dir = Path(source_dir)
        self.structures = {}
        self.globals = {}
        self.key_functions = {}
        
    def analyze_all(self):
        """Run all analysis steps."""
        print("🔍 Analyzing 2048-cli source code...")
        
        # Find main structures
        self.find_structures()
        self.find_globals()
        self.find_key_functions()
        self.analyze_memory_layout()
        
        # Save results
        results = {
            "structures": self.structures,
            "globals": self.globals,
            "functions": self.key_functions,
            "memory_hints": self.get_memory_hints()
        }
        
        with open("experiments/01-source-analysis/structure_analysis.json", "w") as f:
            json.dump(results, f, indent=2)
            
        return results
    
    def find_structures(self):
        """Find struct definitions."""
        print("📊 Finding structures...")
        
        for c_file in self.source_dir.glob("src/*.c"):
            with open(c_file, 'r') as f:
                content = f.read()
                
            # Find struct definitions
            struct_pattern = r'struct\s+(\w+)\s*\{([^}]+)\}'
            for match in re.finditer(struct_pattern, content, re.DOTALL):
                struct_name = match.group(1)
                struct_body = match.group(2)
                
                # Parse fields
                fields = []
                field_pattern = r'(\w+)\s+(\w+)(?:\[([^\]]+)\])?(?:\[([^\]]+)\])?;'
                for field in re.finditer(field_pattern, struct_body):
                    field_info = {
                        "type": field.group(1),
                        "name": field.group(2),
                        "array_dims": []
                    }
                    if field.group(3):
                        field_info["array_dims"].append(field.group(3))
                    if field.group(4):
                        field_info["array_dims"].append(field.group(4))
                    fields.append(field_info)
                
                self.structures[struct_name] = {
                    "file": c_file.name,
                    "fields": fields
                }
        
        # Also check headers
        for h_file in self.source_dir.glob("src/*.h"):
            with open(h_file, 'r') as f:
                content = f.read()
                
            # Look for board/game definitions
            if "board" in content.lower() or "game" in content.lower():
                print(f"  Found relevant header: {h_file.name}")
                # Extract #defines for board size
                for match in re.finditer(r'#define\s+(BOARD_\w+|SIZE\w*)\s+(\d+)', content):
                    print(f"    {match.group(1)} = {match.group(2)}")
    
    def find_globals(self):
        """Find global variables."""
        print("🌐 Finding global variables...")
        
        for c_file in self.source_dir.glob("src/*.c"):
            with open(c_file, 'r') as f:
                content = f.read()
            
            # Find globals (simplified - looks for common patterns)
            # Look for declarations outside functions
            lines = content.split('\n')
            in_function = False
            brace_count = 0
            
            for line in lines:
                # Track if we're in a function
                brace_count += line.count('{') - line.count('}')
                if '{' in line and '(' in line:
                    in_function = True
                elif brace_count == 0:
                    in_function = False
                
                # Look for variable declarations outside functions
                if not in_function and brace_count == 0:
                    # Common patterns for game state
                    if any(keyword in line for keyword in ['board', 'game', 'score', 'grid']):
                        if 'int' in line or 'long' in line or 'struct' in line:
                            print(f"  Potential global in {c_file.name}: {line.strip()}")
                            self.globals[c_file.name] = self.globals.get(c_file.name, [])
                            self.globals[c_file.name].append(line.strip())
    
    def find_key_functions(self):
        """Find key game functions."""
        print("🔧 Finding key functions...")
        
        important_funcs = ['main', 'init', 'move', 'merge', 'add', 'draw', 'input', 'getch', 'score']
        
        for c_file in self.source_dir.glob("src/*.c"):
            with open(c_file, 'r') as f:
                content = f.read()
            
            # Find function definitions
            func_pattern = r'(\w+\s+\*?\s*)(\w+)\s*\([^)]*\)\s*\{'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(2)
                return_type = match.group(1).strip()
                
                # Check if it's an important function
                if any(keyword in func_name.lower() for keyword in important_funcs):
                    self.key_functions[func_name] = {
                        "file": c_file.name,
                        "return_type": return_type
                    }
                    print(f"  Found: {return_type} {func_name}() in {c_file.name}")
    
    def analyze_memory_layout(self):
        """Analyze the likely memory layout."""
        print("💾 Analyzing memory layout...")
        
        # Look specifically for the game board
        for c_file in self.source_dir.glob("src/*.c"):
            if 'engine' in c_file.name or 'game' in c_file.name:
                with open(c_file, 'r') as f:
                    content = f.read()
                
                # Look for 4x4 arrays or 16-element arrays
                if '4][4]' in content or '[16]' in content:
                    print(f"  Found board definition in {c_file.name}")
                    
                    # Extract the specific lines
                    for line in content.split('\n'):
                        if ('4][4]' in line or '[16]' in line) and ('int' in line or 'board' in line):
                            print(f"    {line.strip()}")
    
    def get_memory_hints(self):
        """Generate hints for finding the board in memory."""
        hints = []
        
        # Based on common patterns
        hints.append("Board is likely a 4x4 int array (64 bytes total)")
        hints.append("Empty cells are probably 0")
        hints.append("Cell values are powers of 2: 2, 4, 8, 16, 32...")
        hints.append("Score is likely a 'long' type (8 bytes)")
        hints.append("Look for 16 consecutive integers in memory")
        
        return hints

if __name__ == "__main__":
    analyzer = SourceAnalyzer()
    results = analyzer.analyze_all()
    
    print("\n📋 Analysis Summary:")
    print(f"  Found {len(results['structures'])} structures")
    print(f"  Found {sum(len(v) for v in results['globals'].values())} potential globals")
    print(f"  Found {len(results['functions'])} key functions")
    
    print("\n💡 Memory Search Hints:")
    for hint in results['memory_hints']:
        print(f"  - {hint}")
