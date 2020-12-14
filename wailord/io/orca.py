# -*- coding: utf-8 -*-
"""An ad-hoc treatment of orca output files

This should implement a grammar, but currently consists of a number of utility
structures and functions to parse data from the orca output format

Example:
    See the tests for more

        $ poetry run

Some more details.

Todo:
    * Make grammar
    * Make classes
    * Test the experiments more
    * Pass a list of experiments to ignore
    * Test the ordering of variables
    * Make classes for the order
    * Handle split jobs
    * Propagate exceptions instead of passing the buck with warnings
    * Setup proper logging
    * Scrape NIST Web book for spectra, properties https://webbook.nist.gov/cgi/cbook.cgi?ID=C71432&Mask=800#Electronic-Spec
    * Document more things (e.g. SP -> Single point calculation a.k.a. energy
      calculation)
    * Return interesting things

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import wailord.io as waio
import wailord.utils as wau

import numpy as np
import pandas as pd
import itertools as itertt

import re
import os
import textwrap
import pint
import pint_pandas
import vg

from pathlib import Path
from functools import reduce
from collections import namedtuple, OrderedDict
from operator import itemgetter
from pandas.api.types import CategoricalDtype
from konfik import Konfik

# Pint setup
PA_ = pint_pandas.PintArray
ureg = pint.UnitRegistry()
pint_pandas.PintType.ureg = ureg
Q_ = ureg.Quantity

ureg.define("kcal_mol = kcal / 6.02214076e+23 = kcm")

inpcart = namedtuple("inpcart", "atype x y z")
orcaout = namedtuple("orcaout", "final_energy fGeom basis filename system spin theory")

ORDERED_THEORY = ["HF", "UHF", "QCISD", "CCSD", "QCISD(T)", "CCSD(T)"]

ORDERED_BASIS = [
    "STO-3G",
    "3-21G",
    "6-31G",
    "6-311G",
    "6-311G*",
    "6-311G**",
    "6-311++G**",
    "6-311++G(2d,2p)",
    "6-311++G(2df,2pd)",
    "6-311++G(3df,3pd)",
]

OUT_REGEX = {
    "cartesian_coord": re.compile(r"CARTESIAN\s*COORDINATES\s*\(ANGSTROEM\)\s*"),
    "final_single_point_e": re.compile(r"(?<=FINAL SINGLE POINT ENERGY)\s*-\d*.?\d*"),
    "basis_set": re.compile(r"Orbital\s*basis\s*set\s*information"),
    "MDCI": re.compile(r"The\s*Calculated\s*Surface\s*using\s*the\s*MDCI\s*energy\n"),
    "MDCI w/o Triples": re.compile(
        r"The Calculated Surface using the MDCI energy minus triple correction\s*"
    ),
    "Actual Energy": re.compile(r"The Calculated Surface using the 'Actual Energy'"),
    "SCF Energy": re.compile(r"The Calculated Surface using the SCF energy"),
    "energy_evals": re.compile(r"There will be\s*\d* energy evaluations"),
    "Mulliken": re.compile(r"MULLIKEN ATOMIC CHARGES"),
    "Loewdin": re.compile(r"LOEWDIN ATOMIC CHARGES"),
    "Vibrational Frequencies": re.compile(r"IR SPECTRUM"),
}

# ------------ Refactor


def parseOut(filename, plotter=False):
    """Handles orca outputs with regex for energy and coordinates"""
    intcreg, fsp_ereg, get_basis = itemgetter(
        "cartesian_coord", "final_single_point_e", "basis_set"
    )(OUT_REGEX)
    get_spec = re.compile(r"Number\s*of\s*atoms\s*.*\s*\d*")
    with open(filename) as f:
        fInp = f.read()
        fin_energ = float(fsp_ereg.findall(fInp)[-1].split()[-1]) * ureg.hartree
        if plotter == True:
            energ = [float(x.split()[-1]) for x in fsp_ereg.findall(fInp)]
        num_species = int(get_spec.search(fInp).group(0).split()[-1])
    with open(filename) as f:
        flines = f.readlines()
        allAtoms = []
        for linum, line in enumerate(flines):
            if get_basis.search(line):
                basis = flines[linum + 1].split()[-1]
            if intcreg.search(line):
                offset = linum + 2
                for i in range(num_species):
                    p = flines[offset + i].split()
                    myAtom = inpcart(
                        atype=p[0],
                        x=float(p[1]) * ureg.angstrom,
                        y=float(p[2]) * ureg.angstrom,
                        z=float(p[3]) * ureg.angstrom,
                    )
                    allAtoms.append(myAtom)
    runinfo = getRunInfo(Path(filename).parent)
    if runinfo["spin"] == "spin_01":
        spin = "singlet"
    elif runinfo["spin"] == "spin_03":
        spin = "triplet"
    else:
        raise (NotImplementedError(f"Not yet implemented {runinfo['spin']}"))
    finGeom = []
    for i in reversed(range(1, num_species + 1)):
        finGeom.append(allAtoms[-i])
    #  Creates a dictionary of the system H num O num
    systr = pd.DataFrame(finGeom).atype.value_counts().to_dict()
    # Flattens the dictionary to a list
    listdict = list(itertt.chain.from_iterable(systr.items()))
    # Flattens the list to a single string
    liststr = "".join(map(str, listdict))
    oout = orcaout(
        final_energy=fin_energ,
        fGeom=finGeom,
        basis=basis,
        filename=filename,
        system=liststr,
        spin=spin,
        theory=runinfo["theory"],
    )
    if plotter == True:
        return oout, energ
    else:
        return oout


def get_e(orcaoutdat, basis, system):
    """
    This takes in an orcaout data frame and spits out the energy
    """
    return orcaoutdat[
        (orcaoutdat.basis.isin([basis]) & (orcaoutdat.system.isin([system])))
    ]["final_energy"].to_list()[0]


def getBL(dat, x, y, z, indi=[0, 1]):
    """Takes in a data frame of xyz coordinates and uses it to calculate the bond length"""
    v1 = np.array(
        [dat.x[indi[0]].magnitude, dat.y[indi[0]].magnitude, dat.z[indi[0]].magnitude]
    )
    v2 = np.array(
        [dat.x[indi[1]].magnitude, dat.y[indi[1]].magnitude, dat.z[indi[1]].magnitude]
    )
    return Q_(vg.euclidean_distance(v1, v2), x[indi[0]].units)


def getBA(dat, x, y, z, indi=[0, 1, 2]):
    """Takes in a data frame of xyz coordinates and uses it to generate the
    plane angle, indices are used such that the first is the relative center"""
    v1 = np.array(
        [dat.x[indi[0]].magnitude, dat.y[indi[0]].magnitude, dat.z[indi[0]].magnitude]
    )
    v2 = np.array(
        [dat.x[indi[1]].magnitude, dat.y[indi[1]].magnitude, dat.z[indi[1]].magnitude]
    )
    v3 = np.array(
        [dat.x[indi[2]].magnitude, dat.y[indi[2]].magnitude, dat.z[indi[2]].magnitude]
    )
    v12 = v2 - v1
    v13 = v3 - v1
    return Q_(vg.angle(v12, v13, units="deg"), "degrees")


def genEBASet(
    rootdir,
    deci=3,
    latex=False,
    full=False,
    order_basis=ORDERED_BASIS,
    order_theory=ORDERED_THEORY,
):
    """Takes in a Path object, and typically returns bond angles and energies.
    Optionally returns a TeX table or a full dataset with the filenames and
    geometries. Depreciate this eventually."""
    outs = []
    for root, dirs, files in os.walk(rootdir.resolve()):
        for filename in files:
            if "out" in filename and "slurm" not in filename:
                outs.append(parseOut(f"{root}/{filename}"))
    outdat = pd.DataFrame(data=outs)
    basis_type = CategoricalDtype(categories=order_basis, ordered=True)
    theory_type = CategoricalDtype(categories=order_theory, ordered=True)
    outdat["basis"] = outdat["basis"].astype(basis_type)
    outdat["theory"] = outdat["theory"].astype(theory_type)
    # print(outdat.basis[0])
    # print(pd.DataFrame(outdat.fGeom[0]))
    outdat["angle"] = outdat.fGeom.apply(
        lambda geom: getBA(
            pd.DataFrame(geom),
            pd.DataFrame(geom).x,
            pd.DataFrame(geom).y,
            pd.DataFrame(geom).z,
            [0, 1, 2],
        )
    )
    outdat.sort_values(by=["theory", "basis"], ignore_index=True, inplace=True)
    outdat.final_energy = outdat.final_energy.apply(
        lambda x: np.around(x, decimals=deci)
    )
    outdat.angle = outdat.angle.apply(lambda x: np.around(x, decimals=deci))
    if latex == True:
        return outdat.drop(["filename", "fGeom"], axis=1).to_latex(
            caption="Calculated systems at all basis sets", index=True
        )
    elif full == True:
        return outdat
    else:
        outdat.drop(["filename", "fGeom"], axis=1, inplace=True)
    return outdat


# ------------- Keep ------------------


def getRunInfo(runf):
    """Determines the runtime parameters from the output path

    The implementation uses an ordered dictionary to ensure that the path
    fragments are matched to the correct keys.

    Note:
        This will only work with wailord experiments at the moment

    Args:
        run (:obj:`Path`): Runtime output path
    Returns:
        runinf (:obj:`dict`): A simple unordered dictionary of paramters
    """
    runinf = OrderedDict(
        {"basis": None, "calc": None, "spin": None, "theory": None, "slug": None}
    )
    rfparts = runf.parts
    for num, od in enumerate(runinf, start=1):
        runinf[od] = rfparts[-num]
    runinf["basis"] = runinf["basis"].replace("PP", "++").replace("8", "*")
    runinf["theory"] = runinf["theory"].replace("_", " ")
    return dict(runinf)


class orcaExp:
    """The class meant to handle experiments generated with wailord.

    The general concept is that this is meant to work with the setup wailord
    generates. Remember to use `df.round()` for pretty printing!
    """

    def __init__(
        self, expfolder, deci=3, order_basis=ORDERED_BASIS, order_theory=ORDERED_THEORY
    ):
        """Initializes base parameters


        Args:
            expfolder (:obj:`Path`): Output path to the generated wailord experiment
            order_basis (:obj:`list`, optional): An ordered list for the basis
                sets. Defaults to `ORDERED_BASIS`
            order_theory (:obj:`list`, optional): An ordered list for the basis
                sets. Defaults to `ORDERED_THEORY`. Unlike `order_basis` is can
                vary significantly across experiments.
        """
        self.inpconf = None  #: Populated by `handle_exp`
        self.orclist = None  #: Populated by `handle_exp`
        self.order_basis = order_basis
        self.order_theory = order_theory
        self.handle_exp(expfolder)

    def __repr__(self):
        string = f"""
        Experiment: {self.inpconf}
        Outputs: {self.orclist}
        Ordered Theory: {self.order_theory}
        Ordered Basis: {self.order_basis}
        """
        return textwrap.dedent(string)

    def handle_exp(self, efol):
        """Populates the internal file variables from the path

        Alert:
             This is *not* meant to be called by the user!!!!

        Args:
            efol (:obj:`Path`): Output path

        """
        fnames = []
        self.inpconf = Konfik(config_path=efol / "orca.yml").config
        for root, dirs, files in os.walk(efol.resolve()):
            for filename in files:
                if "out" in filename and "slurm" not in filename:
                    fnames.append(Path(f"{root}/{filename}"))
        self.orclist = fnames
        return

    def get_final_sp_energy(self):
        """Returns a datframe of only the final single point energies

        Proxies calls to the base orcaVis class over a series of generated files

        Args:
            None

        Returns:
            pd.DataFrame: Returns a data frame of final energies
        """
        edatl = []
        for runf in self.orclist:
            runorc = orcaVis(runf).final_sp_e()
            edatl.append(runorc)
        fe = pd.DataFrame(edatl)
        basis_type = CategoricalDtype(categories=self.order_basis, ordered=True)
        theory_type = CategoricalDtype(categories=self.order_theory, ordered=True)
        fe["basis"] = fe["basis"].astype(basis_type)
        fe["theory"] = fe["theory"].astype(theory_type)
        fe.sort_values(
            by=["theory", "basis", "final_sp_energy"], ignore_index=True, inplace=True
        )
        return fe

    def get_vib_freq(self):
        """Returns a datframe of the vibrational frequencies

        Proxies calls to the base orcaVis class over a series of generated files

        Args:
            None

        Returns:
            pd.DataFrame: Returns a data frame of frequencies
        """
        vdatl = []
        for runf in self.orclist:
            runorc = orcaVis(runf).vib_freq()
            vdatl.append(runorc)
        ve = pd.concat(vdatl, axis=0)
        ve = ve.drop_duplicates()
        basis_type = CategoricalDtype(categories=self.order_basis, ordered=True)
        theory_type = CategoricalDtype(categories=self.order_theory, ordered=True)
        ve["basis"] = ve["basis"].astype(basis_type)
        ve["theory"] = ve["theory"].astype(theory_type)
        ve.sort_values(by=["theory", "basis"], ignore_index=True, inplace=True)
        return ve

    def get_energy_surface(self, etype=["Actual Energy", "SCF Energy"]):
        """Populates an energy surface dataframe

        This essentially walks over the generated set of files, and fills out
        calls to the base orcaVis class.

        Args:
            etype (:obj:`list` of :obj:`str`, optional): This is passed to the base
            `OrcaVis` class call

        Returns:
            pd.DataFrame: Returns a data frame of etype energies

        """
        if type(etype) == str:
            etype = [etype]
        edatl = []
        for runf in self.orclist:
            runsurf = orcaVis(runf).mult_energy_surface(etype=etype)
            edatl.append(runsurf)
        edat = pd.concat(edatl, axis=0)
        edat = edat.drop_duplicates()
        basis_type = CategoricalDtype(categories=self.order_basis, ordered=True)
        theory_type = CategoricalDtype(categories=self.order_theory, ordered=True)
        edat["basis"] = edat["basis"].astype(basis_type)
        edat["theory"] = edat["theory"].astype(theory_type)
        edat.sort_values(
            by=["theory", "basis", "bond_length"], ignore_index=True, inplace=True
        )
        return edat

    def get_population(self, poptype=["Mulliken", "Loewdin"], /):
        """Populates a population dataframe

        This essentially walks over the generated set of files, and fills out
        calls to the base orcaVis class.

        Args:
            poptype (:obj:`list` of :obj:`str`, optional): This is passed to the base
            `OrcaVis` class call

        Returns:
            pd.DataFrame: Returns a data frame of etype energies

        """
        if type(poptype) == str:
            poptype = [poptype]
        popdatl = []
        for runf in self.orclist:
            runsurf = orcaVis(runf).mult_population_analysis(poptype)
            popdatl.append(runsurf)
        popdat = pd.concat(popdatl, axis=0)
        popdat = popdat.drop_duplicates()
        basis_type = CategoricalDtype(categories=self.order_basis, ordered=True)
        theory_type = CategoricalDtype(categories=self.order_theory, ordered=True)
        popdat["basis"] = popdat["basis"].astype(basis_type)
        popdat["theory"] = popdat["theory"].astype(theory_type)
        popdat.sort_values(by=["theory", "basis"], ignore_index=True, inplace=True)
        return popdat

    def visit_meta(self, node, visited_children):
        """ Returns the overall output. """
        self.meta = node.text
        return node.text

    def visit_coord_block(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        cb = node.text.split("\n")
        for i, aline in enumerate(cb):
            each = aline.split()
            cb[i] = "    ".join(each)
        self.coord_block = "\n".join(cb)
        # Could have also just returned and assigned node.text
        return node.text


class orcaVis:
    """The class meant to handle ORCA output files.

    Todo:
        * Add a grammar and recursive descent later
    """

    def __init__(self, ofile):
        """Output file initialization.

        This is meant to return base objects to the experiment level class.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            ofile (str): The output file generated by ORCA.
            eeval (int): The number of energy evaluations

        """
        self.eeval = None
        self.ofile = ofile
        self.runinfo = getRunInfo(self.ofile.parent)
        self.fin_sp_e = None
        self.get_evals(self.ofile)
        self.get_final_e()

    def __repr__(self):
        return f"{self.ofile}"

    def get_evals(self, ofile):
        with open(self.ofile) as of:
            flines = of.readlines()
            for line in flines:
                if OUT_REGEX["energy_evals"].search(line):
                    self.eeval = int(line.split()[3])
        return

    def get_final_e(self, dat=False):
        with open(self.ofile) as of:
            fInp = of.read()
            try:
                self.fin_sp_e = (
                    float(
                        OUT_REGEX["final_single_point_e"].findall(fInp)[-1].split()[-1]
                    )
                    * ureg.hartree
                )
            except:
                raise (
                    ValueError(f"Final single point energy not found for {self.ofile}")
                )
        pass

    def final_sp_e(self):
        erow = self.runinfo
        erow["final_sp_energy"] = self.fin_sp_e.m
        erow["unit"] = self.fin_sp_e.u
        return erow

    def mult_energy_surface(
        self,
        etype=["Actual Energy", "MDCI", "MDCI w/o Triples", "SCF Energy"],
        npoints=None,
    ):
        """Multiple Energy surface dataframe generator

        This is a helper function to obtain a dataframe which contains multiple
        energy surfaces. The implementation leverages the `reduce` function from
        `functools` to merge a list of dataframes generated from the
        `single_energy_surface` calls.

        Args:
            etype (str,optional): The type of calculated energy surface to
                return. Defaults to `["Actual Energy", "MDCI", "MDCI w/o Triples",
                "SCF Energy"]` but can be any valid subset of the same.
            npoints (int,optional): The number of points over which a scan has
                taken place. Defaults to the number of evaluations calculated in
                the output file.

        Returns:
            pd.DataFrame: Returns a data frame of bond_length and energies

        .. _MDCI:
            https://www.its.hku.hk/services/research/hpc/software/orca

        """
        if isinstance(etype, str) or len(etype) == 1:
            if isinstance(etype, list):
                etype = etype[0]
            single = self.single_energy_surface(
                etype=etype
            )  #: Short circuit if single type is requested
            for key in self.runinfo.keys():
                single[key] = self.runinfo[key]
            return single
        elist = []
        for et in etype:
            runsurf = self.single_energy_surface(etype=et)
            elist.append(runsurf)
        eDat_all = reduce(lambda df1, df2: pd.merge(df1, df2, on="bond_length"), elist)
        for key in self.runinfo.keys():
            eDat_all[key] = self.runinfo[key]
        return eDat_all

    def single_energy_surface(self, etype="Actual Energy", npoints=None):
        """Single energy surface dataframe generator

        For say, QCISD(T), this is essentially the same as a QCISD calculation.

        Note:
            `MDCI`_ types are meant to work with single reference correlation
            methods

        Args:
            etype (str,optional): The type of calculated energy surface to
            return. Defaults to 'Actual Energy' and can be any of `["Actual Energy", "MDCI", "MDCI w/o Triples", "SCF Energy"]`
            npoints (int,optional): The number of points over which a scan has
                taken place. Defaults to the number of evaluations calculated in
                the output file.

        Returns:
            pd.DataFrame: Returns a data frame of energy surfaces

        .. _MDCI:
            https://www.its.hku.hk/services/research/hpc/software/orca

        """
        if etype not in OUT_REGEX:
            raise (NotImplementedError(f"{etype} has not been implemented yet"))
        if npoints == None:
            npoints = self.eeval
        xaxis = []
        yaxis = []
        sregexp = OUT_REGEX[etype]
        with open(self.ofile) as of:
            flines = of.readlines()
            for lnum, line in enumerate(flines):
                if sregexp.search(line):
                    offset = lnum + 1
                    for i in range(npoints):
                        x, y = flines[offset + i].split()
                        xaxis.append(x)
                        yaxis.append(y)
        edat = pd.DataFrame(
            data=zip(xaxis, yaxis), columns=["bond_length", etype], dtype="float64"
        )
        if edat.empty:
            raise (
                ValueError(f"{etype} surface not found for {self.runinfo['theory']}")
            )
        return edat

    def vib_freq(self):
        """Grabs the non-ZPE corrected IR Spectra and the dipole derivatives for
        intensities"""
        sregexp = OUT_REGEX["Vibrational Frequencies"]
        vline = namedtuple("vline", "Mode freq T2 TX TY TZ")
        accumulate = []
        with open(self.ofile) as of:
            flines = of.readlines()
            for lnum, line in enumerate(flines):
                if sregexp.search(line):
                    offset = lnum + 5
                    i = 0
                    while flines[offset + i] != "\n":
                        raw = flines[offset + i].split()
                        raw = [i for i in raw if i != ":" if i != "(" if i != ")"]
                        v = vline(
                            Mode=int(raw[0].replace(":", "")),
                            freq=float(raw[1]),
                            T2=float(raw[2]),
                            TX=float(raw[3].replace("(", "")),
                            TY=float(raw[4]),
                            TZ=float(raw[5].replace(")", "")),
                        )
                        accumulate.append(v)
                        i = i + 1
        vdat = pd.DataFrame(accumulate)
        vdat["T2"] = vdat["T2"].astype("pint[km/mol]")
        vdat["freq"] = vdat["freq"].astype("pint[cm_1]")
        if vdat.empty:
            raise (
                ValueError(
                    f"Spectra not found for {self.runinfo['theory']}, did you run FREQ?"
                )
            )
        else:
            for key in self.runinfo.keys():
                vdat[key] = self.runinfo[key]
        return vdat

    def single_population_analysis(self, poptype="Mulliken", /):
        """Single population analysis dataframe generator

        Args:
            poptype (str,optional): The type of population analysis to
            return. Defaults to 'Mulliken'.

        Returns:
            pd.DataFrame: Returns a data frame of the population analysis

        """
        if poptype not in OUT_REGEX:
            raise (NotImplementedError(f"{poptype} has not been implemented yet"))
        sregexp = OUT_REGEX[poptype]
        chargeline = namedtuple("chargeline", "anum atype pcharge")
        fulline = namedtuple("fulline", "anum atype pcharge pspin")
        accumulate = []
        with open(self.ofile) as of:
            flines = of.readlines()
            for lnum, line in enumerate(flines):
                if sregexp.search(line):
                    offset = lnum + 2
                    i = 0
                    while (
                        "Sum" not in flines[offset + i]
                        and "--" not in flines[offset + i + 1]
                    ):
                        raw = flines[offset + i].split()
                        if "SPIN" in line:
                            c = fulline(
                                anum=raw[0],
                                atype=raw[1],
                                pcharge=float(raw[-2]),
                                pspin=float(raw[-1]),
                            )
                        else:
                            c = chargeline(
                                anum=raw[0],
                                atype=raw[1],
                                pcharge=float(raw[-1]),
                            )
                        accumulate.append(c)
                        i = i + 1
        popdat = pd.DataFrame(accumulate)
        step = popdat.anum.count() / popdat.anum.nunique()
        popdat["step"] = np.asarray(
            np.repeat(np.arange(1, step + 1), popdat.anum.nunique()), dtype=int
        )
        popdat["population"] = poptype
        if popdat.empty:
            raise (ValueError(f"{poptype} not found for {self.runinfo['theory']}"))
        return popdat

    def mult_population_analysis(self, poptype=["Mulliken", "Loewdin"], /):
        """Multiple population analysis dataframe generator

        This is a helper function to obtain a dataframe which contains multiple
        population analysis outputs. The implementation is similar to the energy surface helper.

        Args:
            poptype (str,optional): The type of calculated energy surface to
                return.

        Returns:
            pd.DataFrame: Returns a data frame of population analysis types
        """
        if isinstance(poptype, str) or len(poptype) == 1:
            if isinstance(poptype, list):
                poptype = poptype[0]
            single = self.single_population_surface(poptype)
            for key in self.runinfo.keys():
                single[key] = self.runinfo[key]
            return single
        poplist = []
        for pt in poptype:
            runsurf = self.single_population_analysis(pt)
            poplist.append(runsurf)
        popdat = reduce(lambda df1, df2: pd.concat([df1, df2]), poplist)
        for key in self.runinfo.keys():
            popdat[key] = self.runinfo[key]
        return popdat
