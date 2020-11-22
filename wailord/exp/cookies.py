"""
A file for rendering cookiecutter templates
"""
from cookiecutter.main import cookiecutter
from pathlib import Path
from konfik import Konfik

from wailord.utils import get_project_root

TEMPLATE_DIR = get_project_root() / "wailord_templates"


def gen_base(template="basicExperiment", absolute=False, filen=None):
    """Generate a base template"""
    if absolute == True:
        template = str(template)
    else:
        template = str(TEMPLATE_DIR / template)
    if filen != None:
        print(filen)
        konfik = Konfik(config_path=filen)
        config = konfik.config
        cookiecutter(
            template,
            no_input=True,
            overwrite_if_exists=True,
            extra_context=config,
            output_dir=config.outdir,
        )
    else:
        # Create project from the basic template
        cookiecutter(template)
