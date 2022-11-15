import wailord.io as waio
import wailord.exp as waex
import pytest
import os
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
        nebr["project_slug"] = "nbr"
        nebr["orca_yml"] = nebr["orca_yml"].replace("brokensym", "basic")
    nbasic = Path(dat / "nbrsym.yml")
    nbasic.write_text(yaml.dump(nebr))
    return nbasic.parent


def test_keywords(datadir):
    """
    Test that ymlt has the same keywords as expected

    Args:
        datadir: write your description
    """
    ymlt = waio.inp.inpGenerator(datadir / "orcaBlockKey.yml")
    string = f"""
    ! NUMGRAD
    ! nofrozencore extremescf vpt2"""
    expect = textwrap.dedent(string)
    ymlt.parse_yml()
    # Kill generated
    shutil.move("harness.sh", "wailordFold")
    shutil.rmtree("wailordFold")
    assert ymlt.keylines == expect
    pass


def test_blocks(datadir):
    """
    Test that ymlt. blocks matches expected blocks

    Args:
        datadir: write your description
    """
    ymlt = waio.inp.inpGenerator(datadir / "orcaBlockKey.yml")
    string = """
    %method
      Z_Tol 1e-14
      SpecialGridAtoms 28, 29, 27
      SpecialGridIntacc 8, 8, 8
    end

    %scf
      rotate {48, 49, 90, 1, 1} end
    end
    """
    expect = textwrap.dedent(string)
    ymlt.parse_yml()
    # Kill generated
    shutil.move("harness.sh", "wailordFold")
    shutil.rmtree("wailordFold")
    assert ymlt.blocks == expect
    pass


def test_geom_constraint(prep_inpgen):
    """
    Test that yaml file has the expected geometry lines

    Args:
        prep_inpgen: write your description
    """
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
        # Kill generated files
        shutil.move("harness.sh", "wailordFold")
        shutil.rmtree("wailordFold")
        ymlt.geomlines == expect
    pass


def test_geom_scaniter(prep_inpgen):
    """
    Test that yaml file has the expected geometry lines

    Args:
        prep_inpgen: write your description
    """
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
        # Kill generated files
        shutil.move("harness.sh", "wailordFold")
        shutil.rmtree("wailordFold")
        ymlt.geomlines == expect
    pass


def test_geom_maxiter(prep_inpgen):
    """
    Test that yaml file has maxiter geometry lines

    Args:
        prep_inpgen: write your description
    """
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
    """
    Test broken symtabs.

    Args:
        prep_inpgen: write your description
    """
    waex.cookies.gen_base(f"{prep_inpgen}/expbrsym.yml")
    pass


def test_nobrsym(prep_inpgen):
    """
    This test is a little lame but it s not a good idea to use this.

    Args:
        prep_inpgen: write your description
    """
    waex.cookies.gen_base(f"{prep_inpgen}/nbrsym.yml")
    pass


def test_viz(datadir):
    """
    Test that the Viz file is properly formatted.

    Args:
        datadir: write your description
    """
    pass


def test_geom_scans(datadir):
    """
    Test that ymlt. geomlines matches the expected geometry lines.

    Args:
        datadir: write your description
    """
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
    # Kill generated
    shutil.move("harness.sh", "wailordFold")
    shutil.rmtree("wailordFold")
    assert ymlt.geomlines == expect
    pass
