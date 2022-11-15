import wailord.io as waio
import wailord.exp as waex
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


@pytest.fixture(scope="session")
def exp_inpgen(tmpdir_factory):
    """Copies folders and fixes input file paths"""
    dat = tmpdir_factory.mktemp("data")
    shutil.copytree(DATADIR, dat, dirs_exist_ok=True)
    with open(f"{dat}/expmult.yml") as fid:
        emult = yaml.full_load(fid)
        emult["outdir"] = f"{dat}/{emult['outdir']}"
        emult["orca_yml"] = f"{dat}/{emult['orca_yml']}"
        emult["inp_xyz"] = f"{dat}/{emult['inp_xyz']}"
    emultsym = Path(f"{dat}/expbrsym.yml")
    emultsym.write_text(yaml.dump(emult))
    return emultsym


def test_multxyz_num(mult_xyz):
    """Checks the number of xyz files"""
    ymlt = waio.inp.inpGenerator(mult_xyz)
    ymlt.parse_yml()
    # Kill generated files
    shutil.move("harness.sh", "wailordFold")
    shutil.rmtree("wailordFold")
    assert len(ymlt.xyz) == 4
    assert len(ymlt.xyzlines) == 4
    pass


def test_multxyz_struct(exp_inpgen):
    """
    Multiply the values in the inpgen dictionary.

    Args:
        exp_inpgen: write your description
    """
    waex.cookies.gen_base(f"{exp_inpgen}")
    pass
