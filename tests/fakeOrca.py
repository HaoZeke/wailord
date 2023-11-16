import wailord.io as waio
from wailord._utils import get_project_root

DATA_DIR = get_project_root() / "tests"

expt = waio.orca.orcaExp(expfolder=DATA_DIR / "io/test_io" / "h2")
