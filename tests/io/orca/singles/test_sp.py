import wailord.io as waio
import pandas as pd
import numpy as np
import warnings
import pytest

from siuba import _, filter, select, mutate

from pint import UnitRegistry
from pathlib import Path

ureg = UnitRegistry()
Q_ = ureg.Quantity
ureg.define("kcal_mol = kcal / 6.02214076e+23 = kcm")

#######################
# Single Energy Tests #
#######################


def test_orca_get_sp_e(datadir):
    sEnerg = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    np.testing.assert_almost_equal(sEnerg.fin_sp_e.m, -1.01010039)
    pass


def test_orca_runinfo(datadir):
    se = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    se.runinfo = waio.orca.getRunInfo(Path("H2_test/QCISD/spin_01/ENERGY/3-21G/"))
    assert se.runinfo == {
        "basis": "3-21G",
        "calc": "ENERGY",
        "spin": "spin_01",
        "theory": "QCISD",
        "slug": "H2_test",
    }
    pass


##########################
# Single Energy Surfaces #
##########################


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


############################
# Multiple Energy Surfaces #
############################


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


##############################
# Single Population Analysis #
##############################


def test_orca_single_chargepop(datadir):
    spop = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    sdat = spop.single_population_analysis()
    assert sdat.shape == (4, 5)
    np.testing.assert_equal(sdat.pcharge.to_numpy(), np.zeros(4))
    sdat2 = spop.single_population_analysis("Loewdin")
    assert sdat2.shape == (4, 5)
    np.testing.assert_equal(sdat2.pcharge.to_numpy(), np.zeros(4))
    pass


def test_orca_single_fullpop(datadir):
    spop = waio.orca.orcaVis(ofile=datadir / "orca_uhf.out")
    sdat = spop.single_population_analysis()
    assert sdat.shape == (2, 6)
    np.testing.assert_equal(sdat.pcharge.to_numpy(), np.zeros(2))
    np.testing.assert_equal(sdat.pspin.to_numpy(), np.zeros(2))
    sdat2 = spop.single_population_analysis("Loewdin")
    assert sdat2.shape == (2, 6)
    np.testing.assert_equal(sdat2.pcharge.to_numpy(), np.zeros(2))
    pass


def test_orca_nstep_pop(datadir):
    spop = waio.orca.orcaVis(ofile=datadir / "ch3f_3ang_b3lyp.out")
    popdat = spop.single_population_analysis()
    assert popdat.step.max() == 2
    assert (popdat >> filter(_.step == 1)).shape == (
        popdat >> filter(_.step == 2)
    ).shape
    pass


################################
# Multiple Population Analysis #
################################


def test_orca_mult_chargepop(datadir):
    spop = waio.orca.orcaVis(ofile=datadir / "orca_qcisdt.out")
    sdat = spop.mult_population_analysis()
    assert sdat.shape == (8, 10)
    np.testing.assert_equal(sdat.pcharge.to_numpy(), np.zeros(8))
    pass


def test_orca_mult_fullpop(datadir):
    spop = waio.orca.orcaVis(ofile=datadir / "orca_uhf.out")
    sdat = spop.mult_population_analysis()
    assert sdat.shape == (4, 11)
    np.testing.assert_equal(sdat.pcharge.to_numpy(), np.zeros(4))
    np.testing.assert_equal(sdat.pspin.to_numpy(), np.zeros(4))
    pass


###############
# IR Spectrum #
###############


def test_orca_irspec(datadir):
    spop = waio.orca.orcaVis(ofile=datadir / "b3lyp_6311g88_h2o.out")
    sdat = spop.ir_spec()
    assert sdat.shape == (3, 11)
    assert sdat.T2.pint.units == "kilometer / mole"
    assert sdat.freq.pint.units == "reciprocal_centimeter"
    np.testing.assert_equal(
        sdat.freq.pint.m.to_numpy(), np.array([1639.47, 3807.28, 3903.73])
    )
    np.testing.assert_equal(sdat.Mode.to_numpy(), np.array([6, 7, 8]))
    pass


#########################
# Vibrational Frequency #
#########################


# FIXME: Test more things
# def test_orca_vibfreq(datadir):
#     spop = waio.orca.orcaVis(ofile=datadir / "orca_imaginary_freq.out")
#     sdat = spop.vib_freq()
#     assert sdat.shape == (3, 33)
#     assert sdat.freq.pint.units == "reciprocal_centimeter"
#     pass


######################
# HTST Rate Constant #
######################


def test_calc_htst(datadir):
    prod = waio.orca.orcaVis(ofile=datadir / "orcaProduct.out")
    react = waio.orca.orcaVis(ofile=datadir / "orcaReactant.out")
    ts = waio.orca.orcaVis(ofile=datadir / "orcaTS.out")
    temp = 298.15
    kf, kb = waio.orca.calc_htst(
        product=prod, reactant=react, transition_state=ts, temperature=temp
    )
    assert kf.u == kb.u
    assert kf.u == "1/second"
    np.testing.assert_almost_equal(kf.m, 2.80583587e-07)
    np.testing.assert_almost_equal(kb.m, 3.31522447e-29)
    pass
