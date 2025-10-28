import os
import sys
import pytest

#pytest -v
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smarthome import SmartHome, Light, Thermostat, Camera, DoorLock, Users

@pytest.fixture(autouse=True)
def reset_state():
    """Сбрасываем состояние SmartHome и Users перед каждым тестом"""
    SmartHome._storage.clear()
    Users._storage.clear()

@pytest.fixture
def home():
    return SmartHome

@pytest.fixture
def admin():
    return Users.add_user("admin", "Admin")

@pytest.fixture
def resident():
    return Users.add_user("resident", "Resident")

@pytest.fixture
def guest():
    return Users.add_user("guest", "Guest")

@pytest.fixture
def lamp():
    return Light(1, "Лампа", 50)

@pytest.fixture
def thermostat():
    return Thermostat(2, "Термостат", 22, 20)

@pytest.fixture
def camera():
    return Camera(3, "Камера")

@pytest.fixture
def doorlock():
    return DoorLock(4, "Замок")
