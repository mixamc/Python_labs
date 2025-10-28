def test_doorlock_unlock_and_lock(doorlock, capsys):
    doorlock.unlock()
    out = capsys.readouterr().out
    assert "открыта" in out
    doorlock.lock()
    out = capsys.readouterr().out
    assert "заперта" in out
