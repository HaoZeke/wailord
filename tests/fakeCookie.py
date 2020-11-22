import wailord.io as waio
import wailord.exp as waex
from wailord.utils import get_project_root

DATA_DIR = get_project_root() / "tests" / "data"

waex.cookies.gen_base(filen=DATA_DIR / "cookieExp.yml")
