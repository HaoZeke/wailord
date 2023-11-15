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

class DotDict(dict):
    """
    Modified dictionary class for accessing key:val via dot notation.
    Inspired by the MIT licensed (defunct) Konfik library
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.keys():
            if isinstance(self[key], dict):
                self[key] = DotDict(self[key])

    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                return super().__getitem__(key)
            except KeyError:
                raise MissingVariableError(f"No such variable '{key}' exists") from None
        else:
            raise TypeError("Key must be a string")

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
        super().__setitem__(key, value)

    def __getattr__(self, key):
        if key.startswith('__') and key.endswith('__'):
            return super().__getattr__(key)
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        if key.startswith('__') and key.endswith('__'):
            super().__setattr__(key, value)
        else:
            self.__setitem__(key, value)

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            super().__delattr__(key)
