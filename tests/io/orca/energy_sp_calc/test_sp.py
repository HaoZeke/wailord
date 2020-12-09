import wailord.io as waio
import pandas as pd
import numpy as np
import warnings
import pytest

from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity

#############################
# Single Energy Evaluations #
#############################


def test_orca_mdci_e_bounds(datadir):
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    with pytest.raises(ValueError):
        sEnerg.single_energy_surface(npoints=34)
    pass


def test_orca_energ_error(datadir):
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    with pytest.raises(NotImplementedError):
        sEnerg.single_energy_surface(etype="Squid")
    pass


def test_orca_energ_empty(datadir):
    warnings.filterwarnings("ignore")
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_uhf.out")
    with pytest.raises(ValueError):
        sEnerg.single_energy_surface("MDCI", 33)
    with pytest.raises(ValueError):
        sEnerg.single_energy_surface("MDCI w/o Triples")
    pass


def test_orca_mdci_e_xvals(datadir):
    """Ensure the bond scan is correct for the MDCI surface"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDat = sEnerg.single_energy_surface("MDCI", 33)
    blength = eDat.bond_length.to_numpy(dtype=float)
    np.testing.assert_almost_equal(
        blength,
        np.linspace(0.4, 2, 33),
    )
    pass


def test_orca_mdci_e_yvals(datadir):
    """Ensure the energy is correct for the MDCI surface"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDat = sEnerg.single_energy_surface("MDCI", 33)
    energy = eDat["MDCI"].to_numpy(dtype=float)
    exp_e = np.array(
        [
            -0.94138797,
            -1.01926347,
            -1.07121343,
            -1.10532121,
            -1.12693056,
            -1.13967221,
            -1.14606214,
            -1.1478773,
            -1.14639965,
            -1.14257386,
            -1.1371073,
            -1.13053326,
            -1.12325284,
            -1.11556491,
            -1.1076896,
            -1.09978747,
            -1.09197505,
            -1.08433716,
            -1.07693613,
            -1.06981843,
            -1.06301908,
            -1.05656468,
            -1.05047427,
            -1.04476152,
            -1.03943444,
            -1.03449586,
            -1.02994375,
            -1.02577148,
            -1.02196149,
            -1.01851026,
            -1.01539626,
            -1.0126,
            -1.01010039,
        ]
    )
    np.testing.assert_almost_equal(
        energy,
        exp_e,
    )
    pass


def test_orca_mdci_e_mtrip_xvals(datadir):
    """Ensure the bond scan is correct for MDCI without triples"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDat = sEnerg.single_energy_surface("MDCI w/o Triples", 33)
    blength = eDat.bond_length.to_numpy(dtype=float)
    np.testing.assert_almost_equal(
        blength,
        np.linspace(0.4, 2, 33),
    )
    pass


def test_orca_mdci_e_mtrip_energy_evals(datadir):
    """Ensure that the number of evaluations matches the number parsed"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDat = sEnerg.single_energy_surface(npoints=33)
    eDat1 = sEnerg.single_energy_surface()
    pd.testing.assert_frame_equal(eDat, eDat1)
    pass


def test_orca_mdci_e_mtrip_yvals(datadir):
    """Ensure the energy is correct for MDCI without triples"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDat = sEnerg.single_energy_surface("MDCI w/o Triples", 33)
    energy = eDat["MDCI w/o Triples"].to_numpy(dtype=float)
    exp_e = np.array(
        [
            -5.94138797,  # Inflated artificially to test
            -1.01926347,
            -1.07121343,
            -1.10532121,
            -1.12693056,
            -1.13967221,
            -1.14606214,
            -1.1478773,
            -1.14639965,
            -1.14257386,
            -1.1371073,
            -1.13053326,
            -1.12325284,
            -1.11556491,
            -1.1076896,
            -1.09978747,
            -1.09197505,
            -1.08433716,
            -1.07693613,
            -1.06981843,
            -1.06301908,
            -1.05656468,
            -1.05047427,
            -1.04476152,
            -1.03943444,
            -1.03449586,
            -1.02994375,
            -1.02577148,
            -1.02196149,
            -1.01851026,
            -1.01539626,
            -1.0126,
            -1.01010039,
        ]
    )
    np.testing.assert_equal(
        energy,
        exp_e,
    )
    pass


###############################
# Multiple Energy Evaluations #
###############################


def test_mult_energy_surf(datadir):
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDat = sEnerg.single_energy_surface("MDCI w/o Triples", 33)
    eDatMDCI = sEnerg.single_energy_surface("MDCI")
    eDatAll = sEnerg.mult_energy_surface()
    pd.testing.assert_frame_equal(eDat, eDatAll[["bond_length", "MDCI w/o Triples"]])
    pd.testing.assert_frame_equal(eDatMDCI, eDatAll[["bond_length", "MDCI"]])
    assert len(eDatAll) == len(eDat)
    pass


def test_mult_energy_surf_subset(datadir):
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDatAll = sEnerg.mult_energy_surface(etype=["MDCI", "SCF Energy"])
    assert "Actual Energy" not in eDatAll.columns
    assert "MDCI" in eDatAll.columns
    assert "SCF Energy" in eDatAll.columns
    pass


def test_mult_energy_surf_single(datadir):
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    eDatSingleL = sEnerg.mult_energy_surface(etype=["MDCI"])
    eDatMDCI = sEnerg.single_energy_surface("MDCI")
    pd.testing.assert_frame_equal(eDatMDCI, eDatSingleL.loc[:, ["bond_length", "MDCI"]])
    eDatSingle = sEnerg.mult_energy_surface(etype="MDCI")
    pd.testing.assert_frame_equal(eDatMDCI, eDatSingle.loc[:, ["bond_length", "MDCI"]])
    pass
