"""XYZ helpers — structured parse via chemparseplot; embed helpers in wailord."""

from __future__ import annotations

import filecmp
from pathlib import Path

import pytest

import wailord.io as waio


def test_coord_block(datadir):
    block = waio.xyz.coord_block(datadir / "h2mol.xyz")
    lines = [ln for ln in block.splitlines() if ln.strip()]
    assert len(lines) == 2
    assert lines[0].split()[0] == "H"
    assert lines[1].split()[0] == "H"


def test_atom_symbols_and_system(datadir):
    path = datadir / "h2mol.xyz"
    assert waio.xyz.atom_symbols(path) == ["H", "H"]
    assert waio.xyz.system_label(path) == "H2"


def test_parse_xyz_via_chemparseplot(datadir):
    pytest.importorskip("parsimonious")
    frame = waio.xyz.parse_xyz(datadir / "h2mol.xyz")
    assert frame.natoms == 2
    assert list(frame.symbols) == ["H", "H"]
    assert frame.system == "H2"
    assert "Avogadro" in frame.comment


def test_rewrite_xyz_preserves_bytes(tmp_path, datadir):
    orig = datadir / "h2mol.xyz"
    dest = tmp_path / "t.xyz"
    waio.xyz.rewrite_xyz(orig, dest)
    assert filecmp.cmp(orig, dest)


def test_write_xyz_roundtrip(tmp_path):
    dest = tmp_path / "w.xyz"
    waio.xyz.write_xyz(
        dest,
        symbols=["H", "H"],
        coordinates=[(0.0, 0.0, 0.0), (0.0, 0.0, 0.74)],
        comment="test",
    )
    assert waio.xyz.atom_symbols(dest) == ["H", "H"]
    assert dest.read_text().splitlines()[0] == "2"
