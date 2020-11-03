import pandas as pd
import wailord.io as waio
from wailord.utils import get_project_root

DATA_DIR = get_project_root() / "tests" / "data"

def test_xyz():
    # Make this more general
    sx = waio.xyz.xyzIO(DATA_DIR/"h2mol.xyz")
    outp = sx.read().split('\n')
    assert len(outp)==4 # Fix later
