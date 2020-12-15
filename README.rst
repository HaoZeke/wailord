=======
Wailord
=======

.. image:: https://w.wallhaven.cc/full/4x/wallhaven-4xgw53.jpg
        :alt: Logo of sorts

.. image:: https://img.shields.io/pypi/v/wailord.svg
        :target: https://pypi.python.org/pypi/wailord

.. image:: https://img.shields.io/travis/HaoZeke/wailord.svg
        :target: https://travis-ci.com/HaoZeke/wailord

.. image:: https://api.netlify.com/api/v1/badges/2209e709-8d41-46ee-bf4d-0b116f9243b1/deploy-status
        :target: https://app.netlify.com/sites/wailord/deploys
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/HaoZeke/wailord/shield.svg
     :target: https://pyup.io/repos/github/HaoZeke/wailord/
     :alt: Updates



Wailord is a python library to interact with ORCA


* Free software: GNU General Public License v3
* Documentation: https://wailord.readthedocs.io. **TBD**


Features
--------

* Integrates with SLURM in a manner of speaking

Limitations
-----------

* By choice, the split-job syntax has not been included in the current formulation
  - The `pre` keyword is a notable exception, as it performs a geometry optimization of the `xyz` file before passing through to the rest of the calculations

Credits
-------

* This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
* The image is from wallhaven.cc

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
