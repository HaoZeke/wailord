"""
A set of functions for rendering cookiecutter templates
"""
from cookiecutter.main import cookiecutter
from pathlib import Path
from konfik import Konfik

from wailord.utils import get_project_root

TEMPLATE_DIR = get_project_root() / "wailord_templates"


def gen_base(filen=None, /, template="basicExperiment", *, absolute=False):
    """Generate a base template"""
    if absolute == True:
        template = str(template)
    else:
        template = str(TEMPLATE_DIR / template)
    if filen is not None:
        konfik = Konfik(config_path=filen)
        config = konfik.config
        if absolute is False:
            config.orca_yml = Path(config.orca_yml).resolve()
            config.inp_xyz = Path(config.inp_xyz).resolve()
        cookiecutter(
            template,
            no_input=True,
            overwrite_if_exists=True,
            extra_context=config,
            output_dir=Path(config.outdir),
        )
    else:
        # Create project from the basic template
        cookiecutter(template)
