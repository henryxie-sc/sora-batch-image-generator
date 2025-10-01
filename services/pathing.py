import sys
from pathlib import Path


def get_app_path() -> Path:
    """Return application root path (supports frozen executable)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent.parent


# Commonly used paths
APP_PATH: Path = get_app_path()
IMAGES_PATH: Path = APP_PATH / "images"

