import wailord.io as waio
import wailord.exp as waex
import pandas as pd
import pytest
import tempfile
import warnings
import textwrap
import yaml
import os
from pathlib import Path
from konfik import Konfik
from shutil import copyfile


def test_geom_maxiter(datadir):
    expect = textwrap.dedent(
    f"""
    %geom
      maxiter = 300
    end
    """)
    with open(f"{datadir}/basic.yml") as baseyml:
        t = yaml.full_load(baseyml)
        t['geom'] = {'maxiter':300}
        tmpyml = tempfile.NamedTemporaryFile('w', suffix = '.yml', delete=False)
        try:
            with tmpyml:
                yaml.dump(t, tmpyml)
                ymlt = waio.inp.inpGenerator(f"{tmpyml.name}")
                copyfile(f"{datadir}/inp.xyz","/tmp/inp.xyz")
                copyfile(f"{datadir}/basejob.sh","/tmp/basejob.sh")
                ymlt.parse_yml()
                ymlt.geomlines == expect
        finally:
            os.unlink(tmpyml.name)
    pass

def test_brokensym(datadir):
    waex.cookies.gen_base(
        template="basicExperiment",
        absolute=False,
        filen=f"{datadir}/expbrsym.yml",
    )
    pass

def test_nobrsym(datadir):
    """Uses temp to rewrite parts of the file"""
    konfik = Konfik(config_path=f"{datadir}/expbrsym.yml")
    config = konfik.config
    config['orca_yml']= config['orca_yml'].replace("brokensym","basic")
    # w is needed for it to be recognized as a file pointer
    tmpyml = tempfile.NamedTemporaryFile('w', suffix = '.yml', delete=False)
    try:
        with tmpyml:
            yaml.dump(dict(config), tmpyml)
        waex.cookies.gen_base(
            filen=f"{tmpyml.name}"
            )
    finally:
        os.unlink(tmpyml.name) # delete
    pass

def test_viz(datadir):
    pass

def test_geom_scans(datadir):
    ymlt = waio.inp.inpGenerator(datadir / "orcaGeom.yml")
    expect = textwrap.dedent(
    f"""
    %geom
      Scan
        B 0 1 = 0.4, 2.0, 17 # Bond scan for C0--H1
        B 0 2 = 0.3, 1.0, 13 # Bond scan for C0--H2
        D 0 1 = 60, 80, 39 # Dihedral scan for C0--H1
        A 0 1 2 = 30, 80, 62 # Angle scan for C0--H1--H2
      end
    end
    """)
    ymlt.parse_yml()
    assert ymlt.geomlines == expect
