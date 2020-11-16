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

inpcart = namedtuple("inpcart", "atype x y z")
orcaout = namedtuple("orcaout", "final_energy fGeom basis filename system")


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
