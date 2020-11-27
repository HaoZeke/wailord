import pandas as pd
import wailord.io as waio
import filecmp, difflib, sys, pytest
from pprint import pprint as ppp
from wailord.utils import get_project_root

from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def test_orca_genEBDA(datadir):
    magnitude = [
        -38.652,
        -38.853,
        -38.864,
        -38.884,
        -38.888,
        -38.889,
        -38.892,
        -38.892,
        -38.892,
    ]
    angles = [
        104.648,
        105.675,
        105.744,
        103.206,
        103.206,
        103.577,
        103.665,
        103.748,
        103.768,
    ]
    sEnerg = waio.orca.genEBASet(datadir / "singlet")
    assert list(sEnerg.final_energy.apply(lambda x: x.magnitude)) == magnitude
    assert list(sEnerg.angle.apply(lambda x: x.magnitude)) == angles
