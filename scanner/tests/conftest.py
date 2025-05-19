from os import path
from sys import path as sys_path

# Ensure the project root is in sys.path for test discovery and imports
PROJECT_ROOT = path.abspath(path.join(path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)
