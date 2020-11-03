from pathlib import Path

def get_project_root() -> Path:
    """
    A helper to obtain the project root path
    """
    return Path(__file__).parent.parent
