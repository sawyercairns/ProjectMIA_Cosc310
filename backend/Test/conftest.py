import sys
from pathlib import Path

# Add /app to sys.path
backend_dir = '/app'
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# CRITICAL: Force pytest to keep /app in sys.path during collection
def pytest_configure(config):
    """Ensure /app stays in sys.path"""
    if '/app' not in sys.path:
        sys.path.insert(0, '/app')

def pytest_collection_modifyitems(session, config, items):
    """Ensure /app is still in sys.path after collection"""
    if '/app' not in sys.path:
        sys.path.insert(0, '/app')