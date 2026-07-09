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
