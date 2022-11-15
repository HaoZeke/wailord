import wailord.io as waio
import pandas as pd
import numpy as np
import pytest

from pint import UnitRegistry
from siuba import _, filter, select, mutate

ureg = UnitRegistry()
Q_ = ureg.Quantity


def test_orca_genEBDA(datadir):
    """
    Test that the genEBDA method works.

    Args:
        datadir: write your description
    """
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
    """
    Test the get_final_sp_energy method of the orca expt module.

    Args:
        datadir: write your description
    """
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
    """
    Test that the get_energy_surface method works correctly with the shape of the energy surface.

    Args:
        datadir: write your description
    """
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
    """
    Test for get_energy_surface with an empty energy surface.

    Args:
        datadir: write your description
    """
    expt = waio.orca.orcaExp(expfolder=datadir / "h2")
    with pytest.raises(ValueError):
        expt.get_energy_surface(etype=["MDCI", "Actual Energy"])
    pass


def test_get_energy_surface_shape_more(datadir):
    """
    Test that the get_energy_surface method works with more shapes.

    Args:
        datadir: write your description
    """
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


#######################
# Population Analysis #
#######################


def test_get_pop(datadir):
    """
    Test that population data is consistent with get_population method.

    Args:
        datadir: write your description
    """
    oth = ["UHF", "UKS BLYP", "UKS B3LYP"]
    expt = waio.orca.orcaExp(expfolder=datadir / "multxyz_pop", order_theory=oth)
    popdat = expt.get_population()
    assert list(popdat.theory.unique()) == [
        "UHF",
        "UKS BLYP",
        "UKS B3LYP",
    ]  #: Increasing level of theory
    assert list(popdat.columns) == [
        "anum",
        "atype",
        "pcharge",
        "pspin",
        "step",
        "population",
        "basis",
        "calc",
        "spin",
        "theory",
        "slug",
    ]
    np.testing.assert_equal(
        popdat.theory.value_counts().to_numpy(),
        np.array([60, 50, 40]),
    )
    pass


###############
# IR Spectrum #
###############


def test_get_ir_freq(datadir):
    """
    Test the get_ir_freq method of the orcaExp class.

    Args:
        datadir: write your description
    """
    oth = ["HF", "MP2", "B3LYP"]
    expt = waio.orca.orcaExp(expfolder=datadir / "ir_spec", order_theory=oth)
    vdat = expt.get_ir_spec()
    assert vdat.shape == (63, 11)
    assert (vdat >> filter(_.slug == "O1H2_h2o")).shape == (9, 11)
    pass


######################
# VPT2 Anharmonicity #
######################


def test_vpt2_transitions(datadir):
    """
    Test that the VPT2 transitions are stored in a transition matrix

    Args:
        datadir: write your description
    """
    oth = ["HF", "MP2", "B3LYP"]
    expt = waio.orca.orcaExp(expfolder=datadir / "vpt2_h2o", order_theory=oth)
    vdat = expt.get_vpt2_transitions()
    assert vdat.shape == (9, 9)
    pass
