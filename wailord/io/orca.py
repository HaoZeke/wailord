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
    * Return interesting things
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import wailord.io as waio
import wailord.utils as wau

import re, itertools, sys, os
from pathlib import Path
from functools import reduce
from collections import namedtuple, OrderedDict
from operator import itemgetter
from pandas.api.types import CategoricalDtype

from pint import UnitRegistry
from konfik import Konfik
import numpy as np
import pandas as pd
import vg

ureg = UnitRegistry()
Q_ = ureg.Quantity

inpcart = namedtuple("inpcart", "atype x y z")
orcaout = namedtuple("orcaout", "final_energy fGeom basis filename system")

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
}


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
    finGeom = []
    for i in reversed(range(1, num_species + 1)):
        finGeom.append(allAtoms[-i])
    #  Creates a dictionary of the system H num O num
    systr = pd.DataFrame(finGeom).atype.value_counts().to_dict()
    # Flattens the dictionary to a list
    listdict = list(itertools.chain.from_iterable(systr.items()))
    # Flattens the list to a single string
    liststr = "".join(map(str, listdict))
    oout = orcaout(
        final_energy=fin_energ,
        fGeom=finGeom,
        basis=basis,
        filename=filename,
        system=liststr,
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


def genEBASet(rootdir, deci=3, latex=False, full=False, order_basis=ORDERED_BASIS):
    """Takes in a Path object, and typically returns bond angles and energies.
    Optionally returns a TeX table or a full dataset with the filenames and
    geometries"""
    outs = []
    for root, dirs, files in os.walk(rootdir.resolve()):
        for filename in files:
            if "out" in filename and "slurm" not in filename:
                outs.append(parseOut(f"{root}/{filename}"))
    outdat = pd.DataFrame(data=outs)
    basis_type = CategoricalDtype(categories=order_basis, ordered=True)
    outdat["basis"] = outdat["basis"].astype(basis_type)
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
    outdat.sort_values(by=["basis"], ignore_index=True, inplace=True)
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


class orcaExp:
    """The class meant to handle experiments generated with wailord.

    The general concept is that this is meant to work with the setup wailord
    generates.
    """

    def __init__(self, inpfile, outfolder, deci=3, order_basis=ORDERED_BASIS):
        self.inpconf = Konfik(config_path=inpfile)
        self.ofolder = outfolder
        self.deci = deci

    def __repr__(self):
        return f"Experiment with {self.inpconf}, and outputs {self.ofolder}"

    def get_energy_surface(self):
        return

    def get_runinfo_path(self, runf):
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
            {"basis": None, "calc": None, "spin": None, "theory": None}
        )
        rfparts = runf.parts
        for num, od in enumerate(runinf, start=1):
            runinf[od] = rfparts[-num]
        runinf["basis"] = runinf["basis"].replace("PP", "++").replace("8", "*")
        return dict(runinf)

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
        self.get_evals(self.ofile)

    def __repr__(self):
        return f"{self.ofile}"

    def get_evals(self, ofile):
        with open(self.ofile) as of:
            flines = of.readlines()
            for line in flines:
                if OUT_REGEX["energy_evals"].search(line):
                    self.eeval = int(line.split()[3])
        return

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
        if type(etype) == str or len(etype) == 1:
            if type(etype) == list:
                etype = etype[0]
            return self.single_energy_surface(
                etype=etype
            )  #: Short circuit if single type is requested
        elist = []
        for et in etype:
            runsurf = self.single_energy_surface(etype=et)
            elist.append(runsurf)
        eDat_all = reduce(lambda df1, df2: pd.merge(df1, df2, on="bond_length"), elist)
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
            pd.DataFrame: Returns a data frame of bond_length and energies

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
        edat = pd.DataFrame(data=zip(xaxis, yaxis), columns=["bond_length", etype])
        return edat
