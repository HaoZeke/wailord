import wailord.io as waio
from wailord.utils import get_project_root

DATA_DIR = get_project_root() / "tests" / "data"

# sorc = waio.orca.orcaIO(DATA_DIR / "orca_opt.out")
sEnerg = waio.orca.genEnergySet(DATA_DIR / "buildOuts")
print(sEnerg)
# print(sEnerg.sort_values(by=["basis"], ascending=False, ignore_index=True))
