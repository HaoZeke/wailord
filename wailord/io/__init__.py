"""I/O package for the wailord batch shell.

Role split (rgpkgs suite):

* **Parse / plot (single file):** ``chemparseplot`` — ``api.parse_xyz``,
  ``api.parse_orca_final_energy``, ``api.extract_orca_geomscan_energy``,
  IR/VPT2/populations under ``chemparseplot.parse.orca``.
* **Single-run ORCA inputs:** ``pychum.render_orca`` (TOML).
* **This package:** multi-job harness generation (``inp``), experiment table
  assembly (``orca.orcaExp``), HTST rates, SLURM-oriented out-file walks, and
  thin XYZ helpers for embedding coordinates in generated inputs.
"""
from . import inp, orca, xyz
