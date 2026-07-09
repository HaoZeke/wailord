"""Suite proxy: wailord I/O prefers chemparseplot when grammar track is present."""

from __future__ import annotations

from pathlib import Path

import pytest

DATA = Path(__file__).parent / "data"
XYZ_FIX = Path(__file__).parent / "io" / "xyz" / "test_xyz" / "h2mol.xyz"


def test_xyz_backend_prefers_chemparseplot_when_available():
    pytest.importorskip("parsimonious")
    try:
        from chemparseplot.parse.grammar.xyz import parse_xyz_file  # noqa: F401
    except ImportError:
        pytest.skip("chemparseplot grammar track not installed")

    import wailord.io as waio

    sx = waio.xyz.xyzIO(XYZ_FIX)
    assert sx._backend == "chemparseplot"
    assert sx.system == "H2"
    assert sx.counts == {"H": 2}


def test_orca_final_energy_proxy_matches_regex(datadir):
    try:
        from chemparseplot.parse.grammar.orca_text import (  # noqa: F401
            parse_orca_text_summary,
        )
    except ImportError:
        pytest.skip("chemparseplot grammar track not installed")

    import wailord.io as waio

    ofile = datadir / "orca_opt.out"
    if not ofile.is_file():
        ofile = DATA / "orca_opt.out"
    # orcaVis needs wailord path layout for runinfo; use parseOut for energy
    # via singles fixtures instead
    sp = (
        Path(__file__).parent
        / "io"
        / "orca"
        / "singles"
        / "test_sp"
        / "orca_qcisdt.out"
    )
    if not sp.is_file():
        pytest.skip("missing orca_qcisdt.out")
    # Temporarily place path under a wailord-like tree is not required for parseOut
    # parseOut needs getRunInfo path structure — call internal helper
    text = sp.read_text()
    e = waio.orca._final_energy_via_chemparseplot(text)
    assert e is not None
    assert e == pytest.approx(-1.01010039, rel=1e-6)


def test_inp_generator_emits_deprecation(tmp_path):
    import warnings

    import yaml

    yml = tmp_path / "t.yml"
    yml.write_text(yaml.dump({"style": "simple", "xyz": "x.xyz"}))
    # Minimal config may still fail later; we only need __init__ warn
    import wailord.io as waio

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            waio.inp.inpGenerator(yml)
        except Exception:
            pass
        dep = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert dep, "expected DeprecationWarning from inpGenerator"
        assert "pychum" in str(dep[0].message).lower()
