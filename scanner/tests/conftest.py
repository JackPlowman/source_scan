from pathlib import Path
from sys import path

# Ensure the project root is in sys.path for test discovery and imports
PROJECT_ROOT = str((Path(__file__).parent.parent.parent).resolve())
if PROJECT_ROOT not in path:
    path.insert(0, PROJECT_ROOT)
