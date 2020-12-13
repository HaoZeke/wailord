"""
This uses wailord functions to generate the experimental structure
"""
import shutil
from pathlib import Path

import wailord.io as waio
from wailord.utils import get_project_root

CUR = Path().absolute()

shutil.copy("{{cookiecutter.orca_yml}}", "orca.yml")
xyzroot = Path("{{cookiecutter.inp_xyz}}")
if xyzroot.is_dir():
    shutil.copytree("{{cookiecutter.inp_xyz}}", f"{xyzroot.stem}")
else:
    shutil.copy("{{cookiecutter.inp_xyz}}", "inp.xyz")
ymlt = waio.inp.inpGenerator(CUR / "orca.yml")
ymlt.prjname = "{{cookiecutter.project_name}}"
ymlt.parse_yml()
