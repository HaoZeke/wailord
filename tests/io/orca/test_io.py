import wailord.io as waio
import pandas as pd
import numpy as np
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


######################
# Final Energy Tests #
######################


def test_get_final_sp_energy(datadir):
    expt = waio.orca.orcaExp(expfolder=datadir / "h2")
    fse = expt.get_final_sp_energy()
    fse.shape == (27, 6)
    fse.final_sp_energy.min() == -1.020894275845
    min_e = fse[fse.final_sp_energy == fse.final_sp_energy.min()]
    max_e = fse[fse.final_sp_energy == fse.final_sp_energy.max()]
    np.testing.assert_equal(
        min_e.values,
        np.array(
            [
                [
                    "6-311++G(3df,3pd)",
                    "ENERGY",
                    "spin_01",
                    "QCISD",
                    "H2_test",
                    -1.020894275845,
                    "hartree",
                ],
                [
                    "6-311++G(3df,3pd)",
                    "ENERGY",
                    "spin_01",
                    "QCISD(T)",
                    "H2_test",
                    -1.020894275845,
                    "hartree",
                ],
            ],
            dtype=object,
        ),
    )
    np.testing.assert_equal(
        max_e.values[0],
        np.array(
            [
                "3-21G",
                "ENERGY",
                "spin_01",
                "UHF",
                "H2_test",
                -0.907804773703,
                "hartree",
            ],
            dtype=object,
        ),
    )
    pass


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
        "slug",
    ]
    assert len(edat[edat.isin(["3-21G"]).any(axis=1)]) == 3 * 33  #: 3 levels of theory
    assert len(edat[edat.isin(["UHF"]).any(axis=1)]) == 9 * 33  #: 9 basis sets
    assert edat.shape == (891, 8)  #: Rows = basis (9) * theory (3) * npoints (33)
    pass


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_get_energy_surface_empty(datadir):
    expt = waio.orca.orcaExp(expfolder=datadir / "h2")
    with pytest.raises(ValueError):
        expt.get_energy_surface(etype=["MDCI", "Actual Energy"])
    pass


def test_get_energy_surface_shape_more(datadir):
    otheory = ["RHF", "RHF MP2", "UHF", "UHF MP2", "QCISD(T)"]
    expt = waio.orca.orcaExp(
        expfolder=datadir / "multiword_energy", order_theory=otheory
    )
    edat = expt.get_energy_surface()
    assert list(edat.theory.unique()) == [
        "RHF",
        "RHF MP2",
        "UHF",
        "UHF MP2",
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
        "slug",
    ]
    np.testing.assert_equal(
        edat.theory.value_counts().to_numpy(),
        np.repeat(33, 5),
    )
    pass
