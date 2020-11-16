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


import re, itertools, sys, os
from pathlib import Path
from collections import namedtuple
from pandas.api.types import CategoricalDtype

from pint import UnitRegistry
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


def parseOut(filename, plotter=False):
    """Handles orca outputs with regex for energy and coordinates"""
    intcreg = re.compile(r"CARTESIAN\s*COORDINATES\s*\(ANGSTROEM\)\s*")
    fsp_ereg = re.compile(r"(?<=FINAL SINGLE POINT ENERGY)\s*-\d*.?\d*")
    get_spec = re.compile(r"Number\s*of\s*atoms\s*.*\s*\d*")
    get_basis = re.compile(r"Orbital\s*basis\s*set\s*information")
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
