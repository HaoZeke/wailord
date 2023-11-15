import wailord.io as waio
from wailord.utils import get_project_root

CONF_DIR = (
    get_project_root()
    / "templates"
    / "basicExperiment"
    / "{{cookiecutter.project_slug}}"
)

DATA_DIR = get_project_root() / "tests" / "data"

# ymlt = waio.inp.inpGenerator(CONF_DIR / "orca.yml")
# ymlt.parse_yml()
# ymlt.gendir_qc()

ymlt = waio.inp.inpGenerator(DATA_DIR / "orcaGeom.yml")
ymlt.parse_yml()
ymlt.gendir_qc()
