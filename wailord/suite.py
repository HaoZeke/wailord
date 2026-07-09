"""Bridge to the rgpkgs suite (rgpycrumbs + chemparseplot).

Wailord is the batch/experiment shell: cookiecutter runs, multi-job tables,
SLURM harnesses. Parse/plot I/O lives in chemparseplot; new ORCA inputs in
pychum. Suite-wide pins, locks, and on-demand imports live in the hub — do
not reimplement them here.

Example::

    from wailord.suite import energy_to_kcal, load_suite_pins, ensure_import

    pins = load_suite_pins()
    kcal = energy_to_kcal(1.0)  # 1 eV -> kcal/mol via chemparseplot.units
"""

from __future__ import annotations

from typing import Any


def load_suite_config():
    """Load merged rgpkgs suite config (``~/.config/rgpkgs`` + project TOML)."""
    from rgpycrumbs.api import load_config

    return load_config()


def load_suite_pins() -> dict[str, str]:
    """Package pins from suite config + ``RGPKGS_LOCK_PINS`` env."""
    try:
        from chemparseplot.api import suite_pins

        return suite_pins()
    except ImportError:
        from rgpycrumbs.api import load_config, pins_from_env

        pins = dict(pins_from_env())
        try:
            pins.update(load_config().merged_package_pins_normalized())
        except Exception:  # noqa: BLE001
            pass
        return pins


def ensure_import(module_name: str):
    """On-demand import via the hub (AUTO_DEPS-aware)."""
    from rgpycrumbs.api import ensure_import as _ensure

    return _ensure(module_name)


def energy_to_kcal(value_eV: Any) -> Any:
    """Convert energy from eV to kcal/mol using chemparseplot units API."""
    from chemparseplot.api import convert_energy_magnitude

    return convert_energy_magnitude(value_eV, "kcal/mol", source_unit="eV")


def energy_to_kJ(value_eV: Any) -> Any:
    """Convert energy from eV to kJ/mol using chemparseplot units API."""
    from chemparseplot.api import convert_energy_magnitude

    return convert_energy_magnitude(value_eV, "kJ/mol", source_unit="eV")
