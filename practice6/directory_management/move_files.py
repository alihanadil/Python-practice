
import os
import sys
import shutil
from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: python move_files.py source_dir dest_dir [extensions...]")
    sys.exit(1)

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
extensions = sys.argv[3:]  # optional list of extensions (e.g., .txt .jpg)

if not src.is_dir():
    print(f"Source directory not found: {src}")
    sys.exit(1)

dst.mkdir(parents=True, exist_ok=True)

for item in src.iterdir():
    if not item.is_file():
        continue
    if extensions and item.suffix not in extensions:
        continue
    try:
        shutil.move(str(item), str(dst / item.name))
        print(f"Moved: {item.name}")
    except Exception as e:
        print(f"Error moving {item.name}: {e}")