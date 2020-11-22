"""
This uses wailord functions to generate the experimental structure
"""
import shutil
from pathlib import Path

import wailord.io as waio
from wailord.utils import get_project_root

CUR = Path().absolute()

print("{{cookiecutter.project_slug}}")
if "{{cookiecutter.orca_yml}}" != "orca.yml":
    shutil.copy("{{cookiecutter.orca_yml}}", "orca.yml")
if "{{cookiecutter.inp_xyz}}" != "inp.xyz":
    shutil.copy("{{cookiecutter.inp_xyz}}", "inp.xyz")
ymlt = waio.inp.inpParser(CUR / "orca.yml")
ymlt.parse_yml()
ymlt.gendir_qc(basename=Path("{{cookiecutter.project_name}}"))
