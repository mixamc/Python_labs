def test_camera_turn_on_and_off(camera, capsys):
    camera.turn_on()
    assert camera.stat
    out = capsys.readouterr().out
    assert "записывает" in out

    camera.turn_off()
    assert not camera.stat
    out = capsys.readouterr().out
    assert "перестала вести запись" in out
