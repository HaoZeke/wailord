from pathlib import Path


def get_project_root() -> Path:
    """
    A helper to obtain the project root path
    From here: https://stackoverflow.com/a/53465812/1895378
    """
    return Path(__file__).parent.parent


def repkey(fname, repobj):
    """
    A helper function to deal with replacements in files
    repobj: A dictionary with "prev" and "to" keys
    """
    assert len(repobj["prev"]) == len(
        repobj["to"]
    ), "The replacement dictionary must contain as many targets as values"
    with open(fname, "r") as f:
        fInp = f.read()
    for p, t in zip(repobj["prev"], repobj["to"]):
        fInp = fInp.replace(p, t)
    with open(fname, "w") as o:
        o.write(fInp)
