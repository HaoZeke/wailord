import wailord.io as waio
import pandas as pd
import pytest
import warnings

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


##############################
# Energy Surface Evaluations #
##############################


def test_get_energy_surface_shape(datadir):
    expt = waio.orca.orcaExp(expfolder=datadir / "h2")
    edat = expt.get_energy_surface()
    assert list(edat.theory.unique()) == [
        "UHF",
        "QCISD",
        "QCISD(T)",
    ]  #: Increasing level of theory
    assert list(edat.columns) == [
        "bond_length",
        "Actual Energy",
        "SCF Energy",
        "basis",
        "calc",
        "spin",
        "theory",
    ]
    assert len(edat[edat.isin(["3-21G"]).any(axis=1)]) == 3 * 33  #: 3 levels of theory
    assert len(edat[edat.isin(["UHF"]).any(axis=1)]) == 9 * 33  #: 9 basis sets
    assert edat.shape == (891, 7)  #: Rows = basis (9) * theory (3) * npoints (33)
    pass

@pytest.mark.filterwarnings("ignore::UserWarning")
def test_get_energy_surface_empty(datadir):
    expt = waio.orca.orcaExp(expfolder=datadir / "h2")
    with pytest.raises(ValueError):
        expt.get_energy_surface(etype=["MDCI", "Actual Energy"])
    pass
