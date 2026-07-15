"""I/O package: thin proxies over the rgpkgs suite where possible.

* ``xyz`` / energy slices → prefer chemparseplot grammar track
  (``chemparseplot.api.parse_xyz``, ``parse_orca_final_energy``,
  ``extract_orca_geomscan_energy``)
* ``inp`` → **frozen**; use pychum for new ORCA inputs
* ``orca`` → experiment helpers (``orcaExp``); parse/plot migrate to chemparseplot
  (see ``chemparseplot.parse.orca.migration.MIGRATION_CHECKLIST``)

Legacy classes emit ``DeprecationWarning`` on construction.
"""
from . import inp, orca, xyz
