"""Suite integration: batch shell uses chemparseplot for structured parse."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

DATA = Path(__file__).parent / "data"
XYZ_FIX = Path(__file__).parent / "io" / "xyz" / "test_xyz" / "h2mol.xyz"


def test_xyz_parse_is_chemparseplot():
    pytest.importorskip("parsimonious")
    import wailord.io as waio

    frame = waio.xyz.parse_xyz(XYZ_FIX)
    assert frame.system == "H2"
    assert list(frame.symbols) == ["H", "H"]


def test_orca_final_energy_via_chemparseplot():
    try:
        from chemparseplot.parse.grammar.orca_text import (  # noqa: F401
            parse_orca_text_summary,
        )
    except ImportError:
        pytest.skip("chemparseplot grammar track not installed")

    import wailord.io as waio

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
    text = sp.read_text()
    e = waio.orca._final_energy_via_chemparseplot(text)
    assert e is not None
    assert e == pytest.approx(-1.01010039, rel=1e-6)


def test_inp_generator_is_batch_api(tmp_path):
    """Multi-job YAML harness remains a first-class batch-shell API (no deprecation)."""
    import warnings

    import wailord.io as waio

    yml = tmp_path / "t.yml"
    yml.write_text(yaml.dump({"style": "simple", "xyz": "x.xyz"}))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        gen = waio.inp.inpGenerator(yml)
        dep = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert not dep, f"unexpected DeprecationWarning: {dep}"
    assert gen.config["xyz"] == "x.xyz"
