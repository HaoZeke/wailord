import wailord.io as waio
from wailord.utils import get_project_root

DATA_DIR = get_project_root() / "tests"

# sorc = waio.orca.orcaIO(DATA_DIR / "orca_opt.out")
# sEnerg = waio.orca.genEBASet(DATA_DIR / "h2")
# print(sEnerg)
# print(sEnerg.sort_values(by=["basis"], ascending=False, ignore_index=True))

# sEnerg = waio.orca.orcaVis(
#     ofile=DATA_DIR / "io/test_io" / "h2/h_h_mol/QCISD(T)/spin_01/ENERGY/3-21G/orca.out"
# )
# print(sEnerg.mult_energy_surface())

expt = waio.orca.orcaExp(expfolder=DATA_DIR / "io/test_io" / "h2")
# edat = expt.get_energy_surface(etype=["MDCI", "Actual Energy"])
