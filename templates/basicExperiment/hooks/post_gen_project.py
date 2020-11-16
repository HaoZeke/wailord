"""
This uses wailord functions to generate the experimental structure
"""
from pathlib import Path

import wailord.io as waio
from wailord.utils import get_project_root

CUR = Path().absolute()

print("{{cookiecutter.project_slug}}")
ymlt = waio.inp.inpParser(CUR / "orca.yml")
ymlt.parse_yml()
ymlt.gendir_qc(basename=Path("{{cookiecutter.project_name}}"))
