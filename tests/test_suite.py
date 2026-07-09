"""wailord uses rgpkgs suite APIs (no local pin/config reimplementation)."""

from __future__ import annotations

import numpy as np

from wailord.suite import energy_to_kcal, load_suite_pins


def test_energy_to_kcal_uses_chemparseplot():
    kcal = float(np.asarray(energy_to_kcal(1.0)).reshape(-1)[0])
    assert 20.0 < kcal < 25.0


def test_load_suite_pins_dict():
    pins = load_suite_pins()
    assert isinstance(pins, dict)


def test_suite_module_does_not_define_private_config_loader():
    import wailord.suite as s
    # bridge only — loaders come from hub
    assert not hasattr(s, "user_config_path") or "rgpycrumbs" in str(
        getattr(s.load_suite_config, "__module__", "")
    )
    assert s.load_suite_config.__module__.startswith("wailord")
    # implementation imports hub
    import inspect
    src = inspect.getsource(s.load_suite_config)
    assert "rgpycrumbs" in src
