# -*- coding: utf-8 -*-
"""An xyz parser

This module implements a grammar for parsing xyz files.

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

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar_xyz = Grammar(
    r"""
    meta = natoms ws coord_block ws?
    natoms = number
    coord_block = (aline ws)+
    aline = (atype ws cline)
    atype = ~"[a-zA-Z]" / ~"[0-9]"
    cline = (float ws float ws float)
    float = pm number "." number
    pm              = ~"[+-]?"
    number          = ~"\\d+"
    ws              = ~"\\s*"
    """
)
"""grammar_xyz: The xyz grammar.

Recall that by default the format `specification for an xyz``
The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""


class xyzVisitor(NodeVisitor):
    """This class extends NodeVisitor"""

    def __init__(self):
        self.natoms = None
        self.coord_block = None
        self.clines = []
        self.atom_types = []
        self.meta = None

    def __repr__(self):
        return f"{self.meta}"

    def visit_meta(self, node, visited_children):
        """ Returns the overall output. """
        self.meta = node.text
        return node.text

    def visit_coord_block(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        self.coord_block = node.text
        return node.text

    def visit_cline(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        self.clines = node.text
        return node.text

    def visit_natoms(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        print(node.text)
        return node.text

    def visit_atype(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        self.atom_types.append(node.text)
        return node.text

    def generic_visit(self, node, visited_children):
        return node.text or visited_children


class xyzIO:
    """This class handles xyz files at a user level"""

    def __init__(self, filename):
        self.filename = filename
        self.comment_line = "Generated by wailord"
        self.xyzdat = None
        self.read()

    def __repr__(self):
        return f"XYZ file {self.filename}"

    def read(self):
        with open(self.filename) as fp:
            dat = fp.readlines()
            self.comment_line = dat[1]
            dat.pop(1)  # Kill comment line
            dat = "".join(map(str, dat))
            sx = xyzVisitor()
            tree = grammar_xyz.parse(dat)
            sx.visit(tree)
            self.xyzdat = sx
            return

    @property
    def comment_line(self):
        return self.__comment_line

    @comment_line.setter
    def comment_line(self, cl):
        if len(cl.split("\n")) > 1:
            cl.replace("\n", " ")
        self.__comment_line = cl

    def write(self, outname):
        with open(outname, "w") as op:
            # Recreate the comment line
            outdat = str(self.xyzdat).split("\n")
            outdat.insert(1, f"{self.comment_line.strip()}")
            op.write("\n".join(outdat))
