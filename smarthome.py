from typing import Dict

class Device:
    def __init__(self, ind: int, name: str):
        self.id = ind
        self.name = name
        self.stat = False

    def turn_off(self):
        if self.stat:
            print(f'Устройство {self.name} отключено.')
            self.stat = False
        else:
            print(f'Устройство {self.name}  уже отключено.')

    def turn_on(self):
        if not self.stat:
            print(f'Устройство {self.name} включено.')
            self.stat = True
        else:
            print(f'Устройство {self.name} уже работает.')

    def status(self):
        print(f'{self.name} - on' if self.stat else f'{self.name} - off')


class Light(Device):
    def __init__(self, ind, name, level: int):
        super().__init__(ind, name)
        self._level = min(abs(level), 100)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, val: int):
        if 0 <= val <= 100:
            self._level = val
            print(f'Изменено значение яркости лампы {self.name} на {self._level}%')
        else:
            print(f'Невозможно поменять значение яркость для лампы {self.name}')


class Thermostat(Device):
    def __init__(self, ind, name, temp, current_temp):
        super().__init__(ind, name)
        self._target = temp
        self.current_temp = current_temp

    @property
    def temperature(self):
        return self._target

    @temperature.setter
    def temperature(self, new: int):
        self._target = new
        print(f'Целевая температура термостата {self.name}: {self._target}')


class Camera(Device):
    def __init__(self, ind, name):
        super().__init__(ind, name)

    def turn_off(self):
        if self.stat:
            print(f'Камера {self.name} перестала вести запись.')
            self.stat = False
        else:
            print(f'Камера {self.name} уже выключена.')

    def turn_on(self):
        if not self.stat:
            print(f'Камера {self.name} записывает.')
            self.stat = True
        else:
            print(f'Камера {self.name} уже записывает.')


class DoorLock(Device):
    def __init__(self, ind, name):
        super().__init__(ind, name)
        self._locked = True

    def lock(self):
        if not self._locked:
            self._locked = True
            print(f'Дверь {self.name} заперта.')
        else:
            print(f'Дверь {self.name} уже заперта.')

    def unlock(self):
        if self._locked:
            self._locked = False
            print(f'Дверь {self.name} открыта.')
        else:
            print(f'Дверь {self.name} уже открыта.')


class Users:
    _storage: Dict[str, str] = dict()
    _roles = ('Admin', 'Resident', 'Guest')

    def __init__(self, name: str = None):
        self.name = name

    @classmethod
    def add_user(cls, name: str, role: str):
        if role in cls._roles:
            cls._storage[name] = role
            print()
            print(f'Добавлен пользователь: {name}')
            return cls(name)
        else:
            print()
            print(f"Нет такой роли пользователя: {role}, пример: {' '.join(i for i in cls._roles)}")
            return None

    @classmethod
    def get_role(cls, name: str):
        return cls._storage.get(name)

    @classmethod
    def get_all_users(cls):
        print()
        print('Информация о всех пользователях: ')
        print('\n'.join('|' + item[0] + ':' + item[1] + '|' for item in cls._storage.items()))


class SmartHome:
    _storage: Dict[int, Device] = dict()

    @classmethod
    def add_device(cls, device: Device):
        print()
        cls._storage[device.id] = device
        print(f'Устройство {device.name} добавлено в умный дом')

    @classmethod
    def del_device(cls, user: Users, idd: int):
        user_name = getattr(user, 'name', None)
        role = Users.get_role(user_name)
        if role != 'Admin':
            print(f'Пользователь {user_name} не имеет права удалять устройства')
            return
        if idd in cls._storage:
            print(f'Устройство {cls._storage[idd].name} удалено из умного дома')
            del cls._storage[idd]
        else:
            print('Устройство не найдено')

    @classmethod
    def get_device_by_id(cls, idd: int):
        return cls._storage.get(idd)

    @classmethod
    def control_device(cls, user: Users, idd: int, command: str, value=None):
        try:
            user_name = getattr(user, 'name', None)
            role = Users.get_role(user_name)
            if role is None:
                print(f'Пользователь {user_name} не найден')
                return
            device = cls._storage.get(idd)
            if device is None:
                print('Устройство не найдено')
                return
            if command == 'delete':
                if role == 'Admin':
                    cls.del_device(user, idd)
                else:
                    print('Нет прав для удаления устройства')
                return
            if command in ('turn_on', 'turn_off'):
                if role == 'Admin':
                    getattr(device, command)()
                elif role == 'Resident':
                    if isinstance(device, (Light, Thermostat)):
                        getattr(device, command)()
                    else:
                        print('Resident не имеет прав на это устройство')
                elif role == 'Guest':
                    if isinstance(device, Light):
                        getattr(device, command)()
                    else:
                        print('Guest может управлять только лампами')
                return
            if command == 'level':
                if not isinstance(device, Light):
                    print('Команда level применима только к лампе')
                    return
                if role in ('Admin', 'Resident'):
                    device.level = value
                else:
                    print('Нет прав для изменения яркости')
                return
            if command == 'temperature':
                if not isinstance(device, Thermostat):
                    print('Команда temperature применима только к термостату')
                    return
                if role in ('Admin', 'Resident'):
                    device.temperature = value
                else:
                    print('Нет прав для изменения температуры')
                return
            if command == 'lock':
                if not isinstance(device, DoorLock):
                    print('Команда lock применима только к DoorLock')
                    return
                if role == 'Admin':
                    device.lock()
                else:
                    print('Только Admin может блокировать дверь')
                return
            if command == 'unlock':
                if not isinstance(device, DoorLock):
                    print('Команда unlock применима только к DoorLock')
                    return
                if role in ('Admin', 'Resident'):
                    device.unlock()
                else:
                    print('Нет прав для открытия двери')
                return
            print('Неизвестная команда')
        except Exception as ex:
            print(f'Ошибка выполнения команды : {ex}')

    @classmethod
    def get_all_devices(cls):
        print()
        print('Информация о всех устройствах: ')
        for idd, device in cls._storage.items():
            print(f'|{idd}: {device.name}|')

if __name__ == "__main__":
    lamp = Light(1, 'Лампа в гостиной', 25)
    term = Thermostat(2, 'Термостат в спальне', 24, 22)
    cam = Camera(3, 'Уличная камера')
    door = DoorLock(4, 'Входная дверь')

    admin = Users.add_user('Михаил', 'Admin')
    resident = Users.add_user('Ирина', 'Resident')
    guest = Users.add_user('Гость', 'Guest')

    SmartHome.add_device(lamp)
    SmartHome.add_device(term)
    SmartHome.add_device(cam)
    SmartHome.add_device(door)

    SmartHome.get_all_devices()

    SmartHome.control_device(admin, 1, 'turn_off')
    SmartHome.control_device(guest, 1, 'turn_on')
    SmartHome.control_device(resident, 1, 'level', value=80)
    SmartHome.control_device(guest, 2, 'temperature', value=26)
    SmartHome.control_device(admin, 4, 'unlock')
    SmartHome.control_device(resident, 4, 'unlock')
    SmartHome.control_device(guest, 4, 'unlock')
    SmartHome.control_device(admin, 3, 'delete')
    SmartHome.get_all_devices()
