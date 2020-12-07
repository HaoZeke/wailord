# -*- coding: utf-8 -*-
"""An orca input generator and reader

This module reads in a configuration file and generates the requisite input
files. It also reads existing configuration files and returns interesting
things. A short description of the input types is at the `ORCA input
description`_ page.

Example:
    See the tests for more

        $ pytest

Some more details.

Todo:
    * Make tests
    * Return interesting things
    * Add MNDO and other semi-empirical methods, which employ a minimal basis by
      default and do not need a basis set in the input
    * Add more explicit support for "simple input lines"
    * Add more explicit support for the "block input structure"
    * Add support for "sequential" jobs
    * Support multiple xyz files
    * Test and expand brokensym
    * Test Visualizer modifications
    * Parse wailord generated input files

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
.. _ORCA input description:
   https://sites.google.com/site/orcainputlibrary/generalinput

"""
import wailord.io as waio
import wailord.utils as wau

import shutil
import textwrap
import itertools as itertt
from pathlib import Path
from operator import itemgetter

from konfik import Konfik

SCAN_TYPES = {"D": "Dihedral", "B": "Bond", "A": "Angle"}
AXIS_PROXY = {"x": 1, "y": 2, "z": 3}  # 0 is the atom type

class inpGenerator:
    def __init__(self, filename):
        self.qc = None
        self.xyz = None
        self.xyzpath = None
        self.spin = None
        self.extra = None
        self.conf_path = Path(filename)
        self.geomlines = None
        self.xyzlines = None
        self.scf = None
        self.viz = None
        self.paramlines = None
        self.konfik = Konfik(config_path=filename)
        self.scripts = []

    def __repr__(self):
        return f"{self.konfik.show_config()}"

    def read_yml(self):
        """ Returns the overall output. """
        self.qc, self.xyzpath, self.spin = itemgetter("qc", "xyz", "spin")(
            self.konfik.config
        )
        # Test this later, with and without, also try overrides
        if "extra" in self.konfik.config.keys():
            self.extra = self.konfik.config.extra
        else:
            print("Consider using None in the yml file for extra")

    def parse_geom(self, geom):
        """Rework the geometry into output"""
        textlines = []
        textlines.append("\n%geom\n")
        if "scan" in geom:
            textlines.append(f"  Scan\n")
            for scanthing in geom.scan.keys():
                if scanthing.capitalize() in SCAN_TYPES.values():
                    textlines.append(
                        self.geom_scan(geom.scan[f"{scanthing}"], scantype=scanthing)
                    )
                else:
                    raise TypeError(
                        f"Only dihedral, bond and angle scan types are supported, got {scanthing} instead"
                    )
            textlines.append(f"  end")
        if "maxiter" in geom:
            textlines.append(textwrap.dedent(f"""
            maxiter {geom.maxiter}
            """))
        textlines.append("\nend\n")
        return "".join(textlines)

    def geom_scan(self, thing, scantype):
        """Handles scans"""
        linesthing = []
        scantype = scantype[0][0].upper()
        for thingline in thing:
            btwn, fromto, points = itemgetter(
                "between",
                "range",
                "points",
            )(thingline)
            comment = self.scan_comment(btwn, scantype)
            linesthing.append(
                f"    {scantype} {btwn} = {fromto[0]}, {fromto[1]}, {points} # {comment}\n"
            )
        return "".join(linesthing)

    def scan_comment(self, between, scantype):
        """Generate a comment line, or raise an error"""
        outtmp = []
        tmp = list(map(int, between.split()))
        thiskey = SCAN_TYPES[f"{scantype}"]
        for i in tmp:
            try:
                outtmp.append(f"{self.xyz.xyzdat.atom_types[i]}{i}")
            except:
                raise SyntaxError(
                    "Trying to use an atom which does not exist, check indices"
                )
        gencom = "--".join(outtmp)
        return f"{thiskey} scan for {gencom}"

    def parse_yml(self):
        """Handle the various options"""
        if self.spin == None:
            # Deal with parsing the basic structure
            self.read_yml()
        if self.xyz == None:
            self.xyz = waio.xyz.xyzIO(self.conf_path.parent / self.konfik.config.xyz)
            self.xyzlines = self.xyz.xyzdat.coord_block
        if self.qc.active == True:
            self.parse_qc()
        # Geometry
        if "geom" in self.konfik.config.keys():
            self.geomlines = self.parse_geom(self.konfik.config.geom)
        # Paramter Blocks
        if "params" in self.konfik.config.keys():
            self.paramlines = self.parse_params(self.konfik.config.params)
        if "scf" in self.konfik.config.keys():
            self.scf = self.parse_scf(self.konfik.config.scf)
        if "viz" in self.konfik.config.keys():
            self.viz = self.parse_viz(self.konfik.config.viz)
        pass

    def parse_viz(self, viz):
        if viz.chemcraft == True:
            return textwrap.dedent("""

            %output
            Print[ P_Basis ] 2
            Print[ P_MOs ] 1
            end

            """)

    def parse_scf(self, scf):
        if "brokensym" not in scf.keys():
            raise(KeyError("Only brokensym is supported"))
        return textwrap.dedent(f"""

        %scf
            BrokenSym {scf.brokensym.more_unpaired}, {scf.brokensym.less_unpaired}
        end

        """)

    def parse_params(self, params):
        """Rework the parameters into output. Recall that these do not require
        relaxation, and can also take fixed variables. On the other hand, these
        need more information to set up."""
        textlines = []
        textlines.append("%paras\n")
        for param in params:
            if param.get("value"):
                param["slot"]["name"] = param["name"]
                self.xyzlines, comment = self.params_slot(param["slot"])
                textlines.append(self.params_value(param, comment))
            elif param.get("range"):
                param["slot"]["name"] = param["name"]
                self.xyzlines, comment = self.params_slot(param["slot"])
                textlines.append(self.params_range(param, comment))
            else:
                raise TypeError(
                    f"Currently only value and range variables are supported"
                )
        textlines.append("end\n")
        return "".join(textlines)

    def params_slot(self, thing):
        if not "xyz" in thing or thing["xyz"] != True:
            raise TypeError("Currently only supports xyz")
        # print(self.xyzlines)
        atype, anum, axis, name = itemgetter("atype", "anum", "axis", "name")(thing)
        xyztmp = self.xyzlines.split("\n")
        aline = xyztmp[anum].split()
        if aline[0] == atype:
            aline[AXIS_PROXY[axis]] = f"{{{name}}}".ljust(15, " ")
            xyztmp[anum] = "    ".join(aline)
        # print("\n".join(xyztmp))
        xyzblock = "\n".join(xyztmp)
        comment = f"# {axis}-axis of {atype}{anum}"
        return xyzblock, comment

    def params_value(self, thing, comment):
        name, val = itemgetter("name", "value")(thing)
        return f"\t{name} = {val} {comment}\n"

    def params_range(self, thing, comment):
        """Handles variables with range"""
        name, lrange, points = itemgetter("name", "range", "points")(thing)
        return f"\t{name} = {lrange[0]}, {lrange[1]}, {points} {comment}\n"

    def genharness(self, basename, slow=False):
        """
        Generate a harness file.

        Args:
            basename (str): The folder into which the harness should be put.
            slow (bool): A parameter used to ensure better practices, rate limits to submitting 10 files every 30 seconds
        Returns:
            Nothing: This generates a file, and nothing else
        """
        with open(f"{basename.parent}/harness.sh", "w") as op:
            op.write("#!/usr/bin/env bash\n")
            op.write("export cur_file=$(realpath $0) \n")
            op.write('export cur_dir=$(dirname "${cur_file}")\n')
            for num, script in enumerate(self.scripts, start=1):
                op.write(f'cd "./{script.parents[0]}"')
                op.write("\n")
                op.write(f"qsub './{script.name}'")
                op.write("\n")
                op.write("cd $cur_dir\n")
                op.write("\n")
                if slow == True:
                    if num % 10 == 0:
                        op.write('echo("Slowing down!")\n')
                        op.write("sleep 30s\n")
        pass

    def parse_qc(self):
        qcList = list(
            itertt.chain(self.qc.style, self.qc.calculations, self.qc.basis_sets)
        )
        self.qcopts = qcList
        pass

    def gendir_qc(self, basename=Path("wailordFold"), extra=None):
        """Function to generate QC folder structure recursively"""
        if extra != None:
            print("Overwriting extra from yml file")
            self.extra = extra
        for styl in self.konfik.config.qc.style:
            styl = styl.replace(" ","_")
            self.gendir_qcspin(basename / styl)
        self.genharness(basename)
        pass

    def gendir_qcspin(self, path):
        """Generates the style folders"""
        for sp in self.spin:
            sp = sp.replace(" ", "")
            self.gendir_qccalc(path / Path(f"spin_{sp}"))
        pass

    def gendir_qccalc(self, path):
        """Generates set of calculation folders"""
        for cal in self.konfik.config.qc.calculations:
            self.gendir_qcbasis(path / cal)
        pass

    def gendir_qcbasis(self, path):
        """Generates the final of input files. Note that the folders will have +
        replaced by P and * by 8"""
        for base in self.konfik.config.qc.basis_sets:
            bas = base.replace("+", "P").replace("*", "8")
            Path.mkdir(path / bas, parents=True, exist_ok=True)
            self.geninp(path / bas)
        pass

    def geninp(self, path):
        """Uses the path to generate details for an input file"""
        tmpstr = str(path).split("/")
        tmpconf = {
            # Reverse the function call order
            "basis": tmpstr[-1].replace("P", "+").replace("8", "*"),
            "calc": tmpstr[-2],
            "spin": " ".join(
                list(itertt.chain.from_iterable(tmpstr[-3].replace("spin_", "")))
            ),
            "style": tmpstr[-4].replace("_", " "),
            "name": path / "orca.inp",
            "unrestricted": False
        }
        if self.scf !=None:
            if tmpconf["style"].find("UKS") != -1  or tmpconf["style"].find("UHF") != -1:
                tmpconf["unrestricted"] = True
        self.writeinp(tmpconf)
        self.putscript(
            to_loc=path,
            from_loc=self.conf_path.parent / self.konfik.config.jobscript,
            slug=f"{tmpconf['basis']}_{tmpconf['style']}",
        )
        pass

    def putscript(self, from_loc, to_loc, slug):
        """Copies the jobscript"""
        shutil.copy(from_loc, to_loc)
        scriptname = to_loc / self.konfik.config.jobscript
        slug = slug.replace(" ","_")
        rep_obj = {
            "prev": ["ORCA_CALCULATION"],
            "to": [slug],
        }
        wau.repkey(scriptname, rep_obj)
        if self.viz != None:
            if self.konfik.config.viz.chemcraft == True:
                with open(scriptname, "a") as script:
                    script.writelines(textwrap.dedent("""
                    cd $SLURM_SUBMIT_DIR
                    $orcadir/orca_2mkl orca -molden"""))
        self.scripts.append(scriptname)
        pass

    def writeinp(self, confobj, extralines=None):
        """Writes an input file. Minimally should have:
        basis, calc, spin, style, name
        extralines: Optional set of lines to write out before the coordinate block
        """
        if extralines == None:
            extralines = self.extra
        basis, calc, spin, style, name, unrestricted = itemgetter(
            "basis",
            "calc",
            "spin",
            "style",
            "name",
            "unrestricted"
        )(confobj)
        with open(name, "w") as op:
            op.write(f"!{style} {basis} {calc}")
            op.write("\n")
            if extralines != None:
                op.write("\n")
                op.writelines(extralines)
                op.write("\n")
            if unrestricted == True:
                op.writelines(self.scf)
            if self.viz != None:
                op.writelines(self.viz)
            if self.paramlines != None:
                op.write("\n")
                op.writelines(self.paramlines)
                op.write("\n")
            if self.geomlines != None:
                op.write("\n")
                op.writelines(self.geomlines)
                op.write("\n")
            op.write(f"*xyz {spin}")
            op.write("\n")
            op.write(self.xyzlines)
            op.write("*")
        pass

class simpleInput:
    """ Base class for representing the simple input line"""
    def __init__(self, data):
        self.contents = None
        return
    def __repr__(self):
        return f"!{contents}"

class blockInput:
    """Base class representing block inputs"""
    def __init__(self, data):
        self.keyword = None
        self.lines = None
        return
    def __repr__(self):
        return textwrap.dedent(f"""
        %block {keyword}
            {lines}
        end
        """)

class coordBlock:
    """Base class for the coordinate block"""
    def __init__(self, data):
        self.keyword = None
        self.lines = None
        return
    def __repr__(self):
        return textwrap.dedent(f"""
        *block {keyword}
            {lines}
        *
        """)

