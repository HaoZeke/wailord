import wailord.io as waio
import wailord.exp as waex
import pandas as pd
import pytest
import tempfile
import warnings
import yaml
import os
from konfik import Konfik

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
    t = dict(config)
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
