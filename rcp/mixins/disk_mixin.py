from rcp.api.consts import DISK_ENDPOINT
from rcp.api.disk import Disk
from rcp.api.storage_profile import StorageProfile
from rcp.api.vdc import Vdc
from rcp.api.vm import Vm


class DiskMixin:

    @classmethod
    def disk_retrieve(cls, id: str) -> Disk:
        """
        Получить объект диска по его ID

        Args:
            id (str): Идентификатор диска

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Disk`
        """
        return Disk().retrieve(id)

    @classmethod
    def disk_create(cls, name: str, size: int, vdc: Vdc or str,
                    storage_profile: StorageProfile or str,
                    wait: bool = True, timeout='default', **kwargs) -> Disk:
        """
        Создать объект

        Args:
            name (str): Имя
            size (int): Размер диска (ГБ)
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            storage_profile (object, str): Объект класса :class:`rcp.api.StorageProfile` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Disk`
        """
        return Disk().create(name=name, size=size, storage_profile=storage_profile,
                             vdc=vdc, wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def disk_update(cls, disk: Disk or str, wait: bool = True, timeout='default', **kwargs) -> Disk:
        """
        Сохранить изменения

        Args:
            disk (object, str): Объект класса :class:`rcp.api.Disk` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Disk`
        """
        if type(disk) is str:
            disk = Disk().retrieve(id=disk)
        return disk.update(wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def disk_delete(cls, disk: Disk or str, wait: bool = True, timeout='default'):
        """
        Удалить объект

        Args:
            disk (object, str): Объект класса :class:`rcp.api.Disk` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if type(disk) is str:
            disk = Disk().retrieve(id=disk)
        disk.delete(wait=wait, timeout=timeout)

    @classmethod
    def disk_attach(cls, disk: Disk or str, vm: Vm or str, wait: bool = True, timeout='default') -> Disk:
        """
        Присоединить существующий во ВЦОДе диск к виртуальному серверу

        Args:
            disk (object, str): Объект класса :class:`rcp.api.Disk` или его id
            vm (object, str): Объект класса :class:`rcp.api.Vm` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ValueError: Если производится попытка сохранить несуществующий
                           объект
            ValueError: Если диск уже присоединен

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Disk`
        """
        if type(disk) is str:
            disk = Disk().retrieve(id=disk)
        elif type(vm) is str:
            vm = Vm().retrieve(id=vm)
        return disk.attach(vm=vm, wait=wait, timeout=timeout)

    @classmethod
    def disk_detach(cls, disk: Disk or str, wait: bool = True, timeout='default') -> Disk:
        """
        Присоединить существующий во ВЦОДе диск к виртуальному серверу

        Args:
            disk (object, str): Объект класса :class:`rcp.api.Disk` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Disk`
        """
        if type(disk) is str:
            disk = Disk().retrieve(id=disk)
        return disk.detach(wait=wait, timeout=timeout)

    @classmethod
    def disk_list(cls, **filters) -> list[Disk]:
        """
        Получить список дисков.

        Args:
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Disk`
        """
        return Disk().get_list(DISK_ENDPOINT, **filters)
