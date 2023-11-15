import wailord.io as waio
import wailord.exp as waex
from wailord._utils import get_project_root

DATA_DIR = get_project_root() / "tests" / "data"

waex.cookies.gen_base(DATA_DIR / "cookieExp.yml")
