0.2.0 (2026-07-19)
------------------

* Finish suite migration (no more deprecation shims):

  * ``xyzIO`` removed — use ``chemparseplot.api.parse_xyz`` /
    ``wailord.io.xyz.parse_xyz``; harness helpers ``coord_block`` /
    ``atom_symbols`` / ``rewrite_xyz``.
  * ``parseOut`` / ``orcaVis`` are private (``_parse_out`` / ``_OrcaRun``);
    public multi-job surface is ``orcaExp`` + ``calc_htst`` / ``genEBASet``.
  * ``inpGenerator`` stays as the multi-job YAML harness (batch shell);
    single-run ORCA inputs remain ``pychum.render_orca``.
* Drop local XYZ grammar; chemparseplot grammar track owns structured XYZ.

0.1.5 (2026-07-19)
------------------

* Raise suite floors to chemparseplot>=1.9.17 and rgpycrumbs>=1.10.10.
* requires-python >=3.11 (matches chemparseplot 1.9.17).
* Restore legacy ``xyzdat.coord_block`` / ``atom_types`` shape when XYZ is
  parsed via chemparseplot so deprecated ``inpGenerator`` still works.
* Document ``wailord[suite]`` as the recommended one-shot install for suite peers.
* Inventory: keep HTST, cookiecutter templates, and SLURM out filters in the
  batch shell; siuba remains absent (not ported).

0.1.4 (2026-07-18)
------------------

* Slim proxy: XYZ and final-energy paths prefer chemparseplot grammar track.
* Proxy vib/IR/VPT2/populations and geomscan through chemparseplot when present.
* Deprecate ``inpGenerator`` in favor of pychum; document migration in README.
* Drop ``vg``; bond lengths/angles use NumPy only (conda-forge friendly metadata).
* Align package license metadata with ``LICENSE`` (GPL-3.0-only).
* Runtime ``install_requires`` are library deps only (no Sphinx/black/flake8).
* Keep exp/cookies and suite bridge as the batch-shell surface.

0.1.3 (2026-07-09)
------------------

* Clean packaging: hatch include/exclude so sdist is package-only (no local venvs).
* Release workflow: PyPI token auth (OIDC publisher not configured) + valid gh release create.

0.1.2 (2026-07-09)
------------------

* Fix CI: pin pandas>=2.2 wheels; move siuba to test extra (old pandas sdist fails on modern Python).
* requires-python >=3.10 for rgpkgs suite deps.
* Yanked on PyPI: contaminated sdist.

0.1.1 (2026-07-09)
------------------

* requires-python >=3.10 (suite deps).
* chemparseplot>=1.9.8, rgpycrumbs>=1.9.18.

=======
History
=======

0.1.0 (2023-11-15)
------------------
* Rewritten from scratch
* Less dependencies

0.0.2 (2020-12-27)
------------------

* Bugfix release
* Added VPT2 calculations

0.0.1 (2020-12-15)
------------------

* First release on PyPI
* IR Spectra
* Energy surfaces (geometry / param)
* Single point calculations
* Multi-run input generators
* Generic syntax helpers for block and keyword inputs  
* Zenodo DOI
* Netlify Docs
