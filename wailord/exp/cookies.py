"""
A set of functions for rendering cookiecutter templates
"""
from cookiecutter.main import cookiecutter
from pathlib import Path
import yaml

from wailord._utils import get_project_root

TEMPLATE_DIR = get_project_root() / "wailord" / "_templates"


def gen_base(filen=None, /, template="basicExperiment", *, absolute=False):
    """Generate a base template"""
    if absolute:
        template = str(template)
    else:
        template = str(TEMPLATE_DIR / template)

    if filen is not None:
        with open(filen, "r") as ymlfile:
            config = yaml.safe_load(ymlfile)

        if not absolute:
            config["orca_yml"] = str(Path(config["orca_yml"]).resolve())
            config["inp_xyz"] = str(Path(config["inp_xyz"]).resolve())

        cookiecutter(
            template,
            no_input=True,
            overwrite_if_exists=True,
            extra_context=config,
            output_dir=Path(config["outdir"]),
        )
    else:
        # Create project from the basic template
        cookiecutter(template)
