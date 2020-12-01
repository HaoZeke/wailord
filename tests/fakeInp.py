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

# # Make this more general
# sx = waio.xyz.xyzIO(DATA_DIR / "h2mol.xyz")
# print(sx.comment_line)
# sx.write("t.xyz")
# from pathlib import Path
# from konfik import Konfik
# import itertools as itertt

# # Define the config path
# BASE_DIR = Path(__file__).parent
# CONFIG_PATH_YML = BASE_DIR / "../templates/baseAssignment/orca.yml"

# # Initialize the konfik class
# konfik = Konfik(config_path=CONFIG_PATH_YML)

# # Print the config file as a Python dict
# konfik.show_config()

# # Get the config dict from the konfik class
# config = konfik.config

# # Handle the config dictionary
# while True:
#     try:
#         print(f"Dictionary length: {len(config)}")
#         item = config.popitem()
#         # Do something with item here...
#         print(f"{item} removed")
#     except KeyError:
#         print("The dictionary has no item now...")
#         break

# for key in config:
#     print(key)

# # possibleConf = [
# #     j for i in itertt.zip_longest(config.qc.calculations, config.basis_sets) for j in i
# # ]

# # for conf in itertt.product(possibleConf):
# #     print(f"{conf} from {len(config.basis_sets)}")


# def genInp(config):
#     pass
#     return


# def countConf(config):
#     pass
#     return numConf
