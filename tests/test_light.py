import pytest

def test_light_default_state(lamp):
    assert lamp.stat is False
    assert 0 <= lamp.level <= 100

def test_light_turn_on_and_off(lamp, capsys):
    lamp.turn_on()
    assert lamp.stat
    lamp.turn_off()
    assert not lamp.stat

def test_light_set_valid_brightness(lamp, capsys):
    lamp.level = 75
    assert lamp.level == 75
    out = capsys.readouterr().out
    assert "Изменено значение яркости" in out

@pytest.mark.parametrize("invalid_value", [-5, 120, 999])
def test_light_set_invalid_brightness(lamp, invalid_value, capsys):
    lamp.level = invalid_value
    out = capsys.readouterr().out
    assert "Невозможно поменять" in out
