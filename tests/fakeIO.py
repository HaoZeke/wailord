import wailord.io as waio
from wailord.utils import get_project_root

DATA_DIR = get_project_root() / "tests" / "data"

# Make this more general
sx = waio.xyz.xyzIO(DATA_DIR / "h2mol.xyz")
print(sx.comment_line)
sx.write("t.xyz")
