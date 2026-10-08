import pytest

from netwatch.stats import summarize


def test_todas_correctas():
    s = summarize([10.0, 12.0, 11.0, 13.0])
    assert s.up is True
    assert s.loss_ratio == 0
    assert s.latency_ms == pytest.approx(11.5)
    # diferencias: 2, 1, 2 -> media 5/3
    assert s.jitter_ms == pytest.approx(5 / 3)


def test_perdida_parcial():
    s = summarize([10.0, None, 20.0, None])
    assert s.up is True
    assert s.loss_ratio == pytest.approx(0.5)
    assert s.latency_ms == pytest.approx(15.0)


def test_todo_perdido():
    s = summarize([None, None, None])
    assert s.up is False
    assert s.loss_ratio == 1
    assert s.latency_ms is None and s.jitter_ms is None


def test_una_sola_muestra_tiene_jitter_cero():
    assert summarize([7.0]).jitter_ms == 0


def test_sin_muestras_da_error():
    with pytest.raises(ValueError):
        summarize([])
