import wailord.io as waio
from wailord._utils import get_project_root

DATA_DIR = get_project_root() / "tests" / "data"

frame = waio.xyz.parse_xyz(DATA_DIR / "h2mol.xyz")
print(frame.comment)
waio.xyz.rewrite_xyz(DATA_DIR / "h2mol.xyz", "t.xyz")
