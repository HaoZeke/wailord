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
  and ``chemparseplot`` (unit helpers). Suite config is shared
  (``~/.config/rgpkgs/config.toml``, project ``rgpkgs.toml``) — wailord does not
  invent its own pin file. See ``wailord.suite``.

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

Migration (rgpkgs suite)
------------------------

Wailord is a **batch / experiment shell** for ORCA workflows. Parsing and
plotting belong in **chemparseplot**; new ORCA inputs belong in **pychum**.

* ``wailord.io.xyz.xyzIO`` → ``chemparseplot.api.parse_xyz`` /
  ``chemparseplot.parse.grammar``
* ``wailord.io.orca.parseOut`` → ``chemparseplot.api.parse_orca_final_energy`` /
  ``parse_orca_text_summary``
* ``wailord.io.orca.orcaVis`` → chemparseplot plot/parse modules for surfaces
* ``wailord.io.inp.inpGenerator`` → ``pychum.render_orca`` (deprecated wrapper)

What stays in wailord (batch shell)::

* Cookiecutter experiment scaffolding (``wailord.exp.cookies``, ``_templates/``)
* HTST rate helper (``wailord.io.orca.calc_htst``) over frequency-job outputs
* SLURM-oriented out-file filters in multi-job table loaders

eOn CON/outcome I/O never lives in wailord — use chemparseplot and
`readcon-core <https://github.com/lode-org/readcon-core>`_ (PyPI:
`readcon <https://pypi.org/project/readcon/>`_). siuba experiment APIs are
not part of the suite and are not ported.
