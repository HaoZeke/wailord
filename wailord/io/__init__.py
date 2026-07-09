"""I/O package: thin proxies over the rgpkgs suite where possible.

* ``xyz`` / energy slices → prefer chemparseplot grammar track
* ``inp`` → deprecated; use pychum for new ORCA inputs
* ``orca`` → experiment helpers; parse/plot migrate to chemparseplot
"""
from . import inp, orca, xyz
