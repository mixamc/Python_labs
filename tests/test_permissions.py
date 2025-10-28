def test_admin_full_access(home, lamp, doorlock, admin, capsys):
    home.add_device(lamp)
    home.add_device(doorlock)

    home.control_device(admin, lamp.id, "turn_on")
    assert lamp.stat

    home.control_device(admin, doorlock.id, "unlock")
    out = capsys.readouterr().out
    assert "открыта" in out

def test_resident_cannot_control_camera(home, camera, resident, capsys):
    home.add_device(camera)
    home.control_device(resident, camera.id, "turn_on")
    out = capsys.readouterr().out
    assert "не имеет прав" in out

def test_guest_can_only_light(home, lamp, thermostat, guest, capsys):
    home.add_device(lamp)
    home.add_device(thermostat)

    home.control_device(guest, lamp.id, "turn_on")
    assert lamp.stat

    home.control_device(guest, thermostat.id, "temperature", value=25)
    out = capsys.readouterr().out
    assert "Нет прав" in out
