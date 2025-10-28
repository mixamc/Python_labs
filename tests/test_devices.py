import pytest
from smarthome import Device

def test_device_init():
    d = Device(1, "TestDevice")
    assert d.id == 1
    assert d.name == "TestDevice"
    assert d.stat is False

def test_device_turn_on_off(capsys):
    d = Device(2, "Light")
    d.turn_on()
    assert d.stat
    out = capsys.readouterr().out
    assert "включено" in out

    d.turn_off()
    assert not d.stat
    out = capsys.readouterr().out
    assert "отключено" in out
