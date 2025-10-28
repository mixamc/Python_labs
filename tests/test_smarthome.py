import pytest

def test_add_and_get_device(home, lamp, capsys):
    home.add_device(lamp)
    out = capsys.readouterr().out
    assert "добавлено" in out
    assert home.get_device_by_id(lamp.id) == lamp

def test_duplicate_add_overwrites(home, lamp):
    home.add_device(lamp)
    home.add_device(lamp)
    assert len(home._storage) == 1

def test_del_device_by_admin(home, lamp, admin, capsys):
    home.add_device(lamp)
    home.del_device(admin, lamp.id)
    out = capsys.readouterr().out
    assert "удалено" in out

def test_del_device_by_non_admin(home, lamp, guest, capsys):
    home.add_device(lamp)
    home.del_device(guest, lamp.id)
    out = capsys.readouterr().out
    assert "не имеет права" in out
