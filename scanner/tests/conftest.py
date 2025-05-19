from os.path import abspath, dirname, join
from sys import path

# Ensure the project root is in sys.path for test discovery and imports
PROJECT_ROOT = abspath(join(dirname(__file__), "..", ".."))
if PROJECT_ROOT not in path:
    path.insert(0, PROJECT_ROOT)
