import pytest

def test_thermostat_init(thermostat):
    assert thermostat.temperature == 22
    assert thermostat.current_temp == 20

def test_thermostat_change_temperature(thermostat, capsys):
    thermostat.temperature = 25
    assert thermostat.temperature == 25
    out = capsys.readouterr().out
    assert "Целевая температура" in out
