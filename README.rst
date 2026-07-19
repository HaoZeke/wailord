=======
Wailord
=======

.. image:: https://raw.githubusercontent.com/HaoZeke/wailord/main/docs/img/cover.jpeg
        :alt: Logo of sorts from wallhaven

.. image:: https://img.shields.io/pypi/v/wailord.svg
        :target: https://pypi.python.org/pypi/wailord

.. image:: https://zenodo.org/badge/303189277.svg
        :target: https://zenodo.org/badge/latestdoi/303189277
        :alt: Zenodo Status

.. image:: https://github.com/HaoZeke/wailord/actions/workflows/build_wailord.yml/badge.svg
        :target: https://github.com/HaoZeke/wailord/actions/workflows/build_wailord.yml
        :alt: Build Status

.. image:: https://api.netlify.com/api/v1/badges/2209e709-8d41-46ee-bf4d-0b116f9243b1/deploy-status
        :target: https://app.netlify.com/sites/wailord/deploys
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/HaoZeke/wailord/shield.svg
     :target: https://pyup.io/repos/github/HaoZeke/wailord/
     :alt: Updates


Wailord is a python library to interact with ORCA_


* Free software: GNU General Public License v3
* Documentation: https://wailord.xyz

Being written up. Till then feel free to use the ZenodoDOI_.


Features
--------

* Part of the **rgpkgs** suite: depends on ``rgpycrumbs`` (config/pins/ensure_import)
  and ``chemparseplot`` (units + parse). Suite config is shared
  (``~/.config/rgpkgs/config.toml``, project ``rgpkgs.toml``). See ``wailord.suite``.
  Parse/plot is chemparseplot; single-run inputs are pychum; wailord is multi-job only.

* Integrates with SLURM in a manner of speaking
* Generic helpers for building arbitrary input files
* Generates data-frames for all supported runs

Limitations
-----------

* By choice, the split-job syntax has not been included

Credits
-------

* Initially conceived during EFN115F_
* This package was based off the `audreyr/cookiecutter-pypackage`_ Cookiecutter_ template
* The image is from `wallhaven.cc`_
* The favicon is from Bulbagarden_

.. _ORCA: https://orcaforum.kofo.mpg.de/
.. _EFN115F: https://notendur.hi.is/~hj/reikniefnafr/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _ZenodoDOI: https://zenodo.org/badge/latestdoi/303189277
.. _Bulbagarden: https://archives.bulbagarden.net/wiki/File:321Wailord_AG_anime.png
.. _`wallhaven.cc`: https://wallhaven.cc/w/4xgw53

Install (rgpkgs suite)
----------------------

Recommended one-shot for the full suite peers (chemparseplot grammar track +
pychum inputs)::

    pip install 'wailord[suite]'

That expands to ``wailord[grammar,pychum]``: grammar-backed XYZ/ORCA text
parsing and modern ORCA input generation. Hard deps already pull
``rgpycrumbs`` and ``chemparseplot``; the suite extra adds the optional
grammar stack and pychum.

Manual peer list (secondary; prefer the suite extra above)::

    pip install 'chemparseplot[grammar]' pychum rgpycrumbs

Role split (rgpkgs suite)
------------------------

Wailord is a **batch / experiment shell** for ORCA workflows.

* **Parse / plot (single file):** ``chemparseplot`` —
  ``api.parse_xyz``, ``api.parse_orca_final_energy``,
  ``api.extract_orca_geomscan_energy``, and
  ``chemparseplot.parse.orca`` (IR / VPT2 / populations / geomscan).
* **Single-run ORCA inputs:** ``pychum.render_orca`` (TOML + dataclasses).
* **Batch shell (this package):**

  * multi-job YAML harness generation (``wailord.io.inp.inpGenerator``)
  * experiment table assembly (``wailord.io.orca.orcaExp``)
  * HTST rates (``calc_htst``) and bond/angle table helpers (``genEBASet``)
  * cookiecutter experiment scaffolding (``wailord.exp.cookies``)
  * thin XYZ embed helpers (``wailord.io.xyz.coord_block``, ``atom_symbols``)

eOn CON/outcome I/O never lives in wailord — use chemparseplot and
`readcon-core <https://github.com/lode-org/readcon-core>`_ (PyPI:
`readcon <https://pypi.org/project/readcon/>`_). siuba experiment APIs are
not part of the suite.
