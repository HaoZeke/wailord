import wailord.io as waio
import wailord.exp as waex
import pytest
import textwrap
import yaml
from pathlib import Path
import shutil

DATADIR: Path = Path(__file__).parent / "test_orcainpgen"


@pytest.fixture(scope="session")
def prep_inpgen(tmpdir_factory):
    """Copies folders and fixes input file paths"""
    dat = tmpdir_factory.mktemp("data")
    shutil.copytree(DATADIR, dat, dirs_exist_ok=True)
    # Rework the broken symmetry file
    with open(f"{dat}/expbrsym.yml") as fid:
        ebr = yaml.full_load(fid)
        ebr["outdir"] = f"{dat}/{ebr['outdir']}"
        ebr["orca_yml"] = f"{dat}/{ebr['orca_yml']}"
        ebr["inp_xyz"] = f"{dat}/{ebr['inp_xyz']}"
    ebrsym = Path(f"{dat}/expbrsym.yml")
    ebrsym.write_text(yaml.dump(ebr))
    # Create a file without broken symmetry
    with open(f"{dat}/expbrsym.yml") as fid:
        nebr = yaml.full_load(fid)
        nebr["orca_yml"] = nebr["orca_yml"].replace("brokensym", "basic")
    nbasic = Path(dat / "nbrsym.yml")
    nbasic.write_text(yaml.dump(nebr))
    return nbasic.parent


def test_geom_constraint(prep_inpgen):
    string = f"""
    %geom
      Scan
        B 0 1 = 0.4, 2.0, 17 # Bond scan for C0--H1
        B 0 2 = 0.3, 1.0, 13 # Bond scan for C0--H2
        D 0 1 = 60, 80, 39 # Dihedral scan for C0--H1
        A 0 1 2 = 30, 80, 62 # Angle scan for C0--H1--H2
      end
      Constraints
        {{ B 0 1 30.0 C }} # Bond constraint on C0--H1
        {{ B 0 2  C }} # Bond constraint on C0--H2
      end
      maxiter = 300
    end
    """
    expect = textwrap.dedent(string)
    with open(f"{prep_inpgen}/orcaGeom.yml") as baseyml:
        t = yaml.full_load(baseyml)
        t["geom"].update({"maxiter": 300})
        tyml = Path(prep_inpgen / "tyml.yml")
        tyml.write_text(yaml.dump(t))
        ymlt = waio.inp.inpGenerator(tyml)
        ymlt.parse_yml()
        ymlt.geomlines == expect
    pass


def test_geom_scaniter(prep_inpgen):
    string = f"""
    %geom
      Scan
        B 0 1 = 0.4, 2.0, 17 # Bond scan for C0--H1
        B 0 2 = 0.3, 1.0, 13 # Bond scan for C0--H2
        D 0 1 = 60, 80, 39 # Dihedral scan for C0--H1
        A 0 1 2 = 30, 80, 62 # Angle scan for C0--H1--H2
      end
      maxiter = 300
    end
    """
    expect = textwrap.dedent(string)
    with open(f"{prep_inpgen}/orcaGeom.yml") as baseyml:
        t = yaml.full_load(baseyml)
        t.pop("constraints", None)
        t["geom"].update({"maxiter": 300})
        tyml = Path(prep_inpgen / "tyml.yml")
        tyml.write_text(yaml.dump(t))
        ymlt = waio.inp.inpGenerator(tyml)
        ymlt.parse_yml()
        ymlt.geomlines == expect
    pass


def test_geom_maxiter(prep_inpgen):
    string = f"""
    %geom
      maxiter = 300
    end
    """
    expect = textwrap.dedent(string)
    with open(f"{prep_inpgen}/basic.yml") as baseyml:
        t = yaml.full_load(baseyml)
        t["geom"] = {"maxiter": 300}
        tyml = Path(prep_inpgen / "tyml.yml")
        tyml.write_text(yaml.dump(t))
        ymlt = waio.inp.inpGenerator(tyml)
        ymlt.parse_yml()
        ymlt.geomlines == expect
    pass


def test_brokensym(prep_inpgen):
    waex.cookies.gen_base(f"{prep_inpgen}/expbrsym.yml")
    pass


def test_nobrsym(prep_inpgen):
    waex.cookies.gen_base(f"{prep_inpgen}/nbrsym.yml")
    pass


def test_viz(datadir):
    pass


def test_geom_scans(datadir):
    ymlt = waio.inp.inpGenerator(datadir / "orcaGeom.yml")
    string = f"""
    %geom
      Scan
        B 0 1 = 0.4, 2.0, 17 # Bond scan for C0--H1
        B 0 2 = 0.3, 1.0, 13 # Bond scan for C0--H2
        D 0 1 = 60, 80, 39 # Dihedral scan for C0--H1
        A 0 1 2 = 30, 80, 62 # Angle scan for C0--H1--H2
      end
      Constraints
        {{ B 0 1 30.0 C }} # Bond constraint on C0--H1
        {{ B 0 2  C }} # Bond constraint on C0--H2
      end
    end
    """
    expect = textwrap.dedent(string)
    ymlt.parse_yml()
    assert ymlt.geomlines == expect