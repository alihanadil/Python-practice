
import os
import sys
from pathlib import Path

# Determine base directory: first argument if provided and not starting with '-'
if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
    base = Path(sys.argv[1])
    dir_names = sys.argv[2:]  # remaining args are directory names
else:
    base = Path.cwd()
    dir_names = sys.argv[1:]  # if no base, all args are dir names

# If no directory names given, read from stdin (e.g., from a file)
if not dir_names:
    dir_names = [line.strip() for line in sys.stdin if line.strip()]

if not dir_names:
    print("No directory names provided.")
    sys.exit(1)

for name in dir_names:
    target = base / name
    try:
        target.mkdir(parents=True, exist_ok=True)
        print(f"Created: {target}")
    except Exception as e:
        print(f"Failed to create {target}: {e}")