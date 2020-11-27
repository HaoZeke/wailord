import wailord.io as waio
import pandas as pd
import numpy as np
import filecmp, difflib, sys, pytest
from pprint import pprint as ppp
from wailord.utils import get_project_root

from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def test_orca_mdci_e_bounds(datadir):
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_energy.out")
    with pytest.raises(ValueError):
        sEnerg.mdci_e(34)


def test_orca_mdci_e_xvals(datadir):
    """Ensure the bond scan is correct for the MDCI surface"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_energy.out")
    eDat = sEnerg.mdci_e(33)
    blength = eDat.bond_length.to_numpy(dtype=float)
    np.testing.assert_almost_equal(
        blength,
        np.linspace(0.4, 2, 33),
    )


def test_orca_mdci_e_yvals(datadir):
    """Ensure the energy is correct for the MDCI surface"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_energy.out")
    eDat = sEnerg.mdci_e(33)
    energy = eDat.mdci_energy.to_numpy(dtype=float)
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


def test_orca_mdci_e_mtrip_xvals(datadir):
    """Ensure the bond scan is correct for MDCI without triples"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_energy.out")
    eDat = sEnerg.mdci_e_mtrip(33)
    blength = eDat.bond_length.to_numpy(dtype=float)
    np.testing.assert_almost_equal(
        blength,
        np.linspace(0.4, 2, 33),
    )


def test_orca_mdci_e_mtrip_yvals(datadir):
    """Ensure the energy is correct for MDCI without triples"""
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_energy.out")
    eDat = sEnerg.mdci_e_mtrip(33)
    energy = eDat.mdci_no_triples.to_numpy(dtype=float)
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
