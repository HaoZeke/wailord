# -*- coding: utf-8 -*-
"""An xyz parser

This module implements a grammar for parsing xyz files.

Example:
    See the tests for more

        $ poetry run

Some more details.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(
    r"""
    meta = natoms ws coord_block ws?
    natoms = number
    coord_block = (aline ws)+
    aline = (atype ws cline)
    atype = ~"[a-zA-Z]" / ~"[0-9]"
    cline = (float ws float ws float)
    float = pm number "." number
    pm              = ~"[+-]?"
    number          = ~"\d+"
    ws              = ~"\s*"
    """
)

class xyzVisitor(NodeVisitor):
    def visit_meta(self, node, visited_children):
        """ Returns the overall output. """
        output = {}
        print("meta")
        print(node.text)
        return output
    def visit_coord_block(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        print("coord_block")
        print(node.text)
        return
    def visit_cline(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        print("cline")
        print(node.text)
        return
    def visit_natoms(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        print("natoms")
        return
    def visit_comment(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        print("comment")
        print(node.text)
        return
    def visit_atom_type(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        print("atom_type")
        return
    def generic_visit(self, node, visited_children):
        return node.text or visited_children


class xyzIO():
    comment_line = None
    def __init__(self, filename):
        self.filename = filename
    def read(self):
        with open(self.filename) as fp:
            dat = fp.readlines()
            self.comment_line = dat[1]
            dat.pop(1) # Kill comment line
            dat = ''.join(map(str,dat))
            sx = xyzVisitor()
            tree = grammar.parse(dat)
            return sx.visit(tree)
