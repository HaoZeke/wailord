import pandas as pd
import wailord.io as waio
import filecmp, difflib, sys
from pprint import pprint as ppp
from wailord.utils import get_project_root

DATA_DIR = get_project_root() / "tests" / "data"

# def test_xyz():
#     # Make this more general
#     sx = waio.xyz.xyzIO(DATA_DIR/"h2mol.xyz")
#     outp = sx.read().split('\n')
#     assert len(outp)==4 # Fix later


def printDiff(f1, f2):
    """
    Helper function to diagnose errors between files
    """
    diff = difflib.Differ()
    with open(f1) as fo1:
        f1t = fo1.read()
    with open(f2) as fo2:
        f2t = fo2.read()
    res = difflib.unified_diff(f1t, f2t)
    sys.stdout.writelines(res)

def test_write_xyz(tmp_path):
    """
    The write test
    """
    d = tmp_path / "xyz"
    d.mkdir()
    orig = DATA_DIR / "h2mol.xyz"
    testout = d / "t.xyz"
    sx = waio.xyz.xyzIO(orig)
    sx.write(testout)
    res = filecmp.cmp(orig, testout)
    if res == False:
        printDiff(orig, testout)
    assert res == True
