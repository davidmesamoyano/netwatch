import pytest

from netwatch.config import load_config


def write(tmp_path, text):
    p = tmp_path / "config.yaml"
    p.write_text(text, encoding="utf-8")
    return p


def test_carga_ejemplo():
    cfg = load_config("config.example.yaml")
    assert len(cfg.targets) == 5
    assert {t.kind for t in cfg.targets} == {"simulada", "real"}


def test_kind_invalido(tmp_path):
    with pytest.raises(ValueError):
        load_config(write(tmp_path, "targets:\n  - {name: a, host: x, kind: otro}\n"))


def test_sin_destinos(tmp_path):
    with pytest.raises(ValueError):
        load_config(write(tmp_path, "interval_seconds: 5\n"))


def test_nombres_duplicados(tmp_path):
    with pytest.raises(ValueError):
        load_config(write(tmp_path, "targets:\n  - {name: a, host: x}\n  - {name: a, host: y}\n"))
