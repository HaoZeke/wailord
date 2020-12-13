import wailord.io as waio
import pytest
import yaml
import shutil
from pathlib import Path

DATADIR: Path = Path(__file__).parent / "test_multxyz"


@pytest.fixture(scope="session")
def mult_xyz(tmpdir_factory):
    """Copies folders and fixes input file paths"""
    dat = tmpdir_factory.mktemp("data")
    shutil.copytree(DATADIR, dat, dirs_exist_ok=True)
    with open(f"{dat}/orcaMultxyz.yml") as mxyz:
        t = yaml.full_load(mxyz)
        t["xyz"] = f"{dat}/{t['xyz']}"
        fn = Path(dat / "omult.yml")
        fn.write_text(yaml.dump(t))
    return fn


def test_multxyz_num(mult_xyz):
    """Checks the number of xyz files"""
    ymlt = waio.inp.inpGenerator(mult_xyz)
    ymlt.parse_yml()
    # Move generated files
    shutil.move("wailordFold", mult_xyz.parent)
    shutil.move("harness.sh", mult_xyz.parent)
    assert len(ymlt.xyz) == 4
    assert len(ymlt.xyzlines) == 4
    pass


def test_multxyz_struct(mult_xyz):
    pass
