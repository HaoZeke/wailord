from pathlib import Path


def get_project_root() -> Path:
    """
    A helper to obtain the project root path
    From here: https://stackoverflow.com/a/53465812/1895378
    """
    return Path(__file__).parent.parent
