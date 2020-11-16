# -*- coding: utf-8 -*-
"""An orca input generator

This module reads in a configuration file and generates the requisite input
files

Example:
    See the tests for more

        $ poetry run

Some more details.

Todo:
    * Make tests
    * Return interesting things
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import wailord.io as waio

import shutil
import itertools as itertt
from pathlib import Path
from operator import itemgetter

from konfik import Konfik


class inpParser:
    def __init__(self, filename):
        self.qc = None
        self.xyz = None
        self.xyzpath = None
        self.spin = None
        self.extra = None
        self.conf_path = filename
        self.konfik = Konfik(config_path=filename)
        self.scripts = []

    def __repr__(self):
        return f"{self.konfik.show_config()}"

    def read_yml(self):
        """ Returns the overall output. """
        print("Populating items")
        self.qc, self.xyzpath, self.spin = itemgetter("qc", "xyz", "spin")(
            self.konfik.config
        )
        # Test this later, with and without, also try overrides
        if "extra" in self.konfik.config.keys():
            self.extra = self.konfik.config.extra
        else:
            print("Consider using None in the yml file for extra")

    def parse_yml(self):
        """Handle the various options"""
        if self.spin == None:
            # Deal with parsing the basic structure
            self.read_yml()
        if self.xyz == None:
            self.xyz = waio.xyz.xyzIO(self.conf_path.parent / self.konfik.config.xyz)
        if self.qc.active == True:
            self.parse_qc()

    def genharness(self, basename, slow=False):
        with open(f"{basename}/harness.sh", "w") as op:
            op.write("#!/usr/bin/env bash\n")
            for num, script in enumerate(self.scripts, start=1):
                op.write(f"qsub ./{script}")
                op.write("\n")
                if slow == True:
                    if num % 10 == 0:
                        op.write('echo("Slowing down!")\n')
                        op.write("sleep 30s\n")

    def parse_qc(self):
        print("Parsing QC")
        qcList = list(
            itertt.chain(self.qc.style, self.qc.calculations, self.qc.basis_sets)
        )
        self.qcopts = qcList

    def gendir_qc(self, basename=Path("wailordFold"), extra=None):
        """Function to generate QC folder structure recursively"""
        if extra != None:
            print("Overwriting extra from yml file")
            self.extra = extra
        for styl in self.konfik.config.qc.style:
            self.gendir_qcspin(basename / styl)
        self.genharness(basename)

    def gendir_qcspin(self, path):
        """Generates the style folders"""
        for sp in self.spin:
            sp = sp.replace(" ", "")
            self.gendir_qccalc(path / Path(f"spin_{sp}"))

    def gendir_qccalc(self, path):
        """Generates set of calculation folders"""
        for cal in self.konfik.config.qc.calculations:
            self.gendir_qcbasis(path / cal)

    def gendir_qcbasis(self, path):
        """Generates the final of input files"""
        for base in self.konfik.config.qc.basis_sets:
            Path.mkdir(path / base, parents=True, exist_ok=True)
            self.geninp(path / base)

    def geninp(self, path):
        """Uses the path to generate details for an input file"""
        tmpstr = str(path).split("/")
        tmpconf = {
            # Reverse the function call order
            "basis": tmpstr[-1],
            "calc": tmpstr[-2],
            "spin": " ".join(
                list(itertt.chain.from_iterable(tmpstr[-3].replace("spin_", "")))
            ),
            "style": tmpstr[-4],
            "name": path / "orca.inp",
        }
        self.writeinp(tmpconf)
        self.putscript(
            to_loc=path, from_loc=self.conf_path.parent / self.konfik.config.jobscript
        )

    def putscript(self, from_loc, to_loc):
        """Copies the jobscript"""
        shutil.copy(from_loc, to_loc)
        self.scripts.append(to_loc / self.konfik.config.jobscript)

    def writeinp(self, confobj, extralines=None):
        """Writes an input file. Minimally should have:
        basis, calc, spin, style, name
        extralines: Optional set of lines to write out before the coordinate block
        """
        if extralines == None:
            extralines = self.extra
        basis, calc, spin, style, name = itemgetter(
            "basis",
            "calc",
            "spin",
            "style",
            "name",
        )(confobj)
        with open(name, "w") as op:
            op.write(f"!{style} {basis} {calc}")
            op.write("\n")
            if extralines != None:
                op.write("\n")
                op.writelines(extralines)
                op.write("\n")
            op.write(f"*xyz {spin}")
            op.write("\n")
            op.write(self.xyz.xyzdat.coord_block)
            op.write("*")
