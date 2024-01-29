from rcp.api.network import Network
from rcp.api.port import Port
from rcp.api.vdc import Vdc
from rcp.api.vm import Vm
from rcp.api.router import Router


class PortMixin:

    @classmethod
    def port_retrieve(cls, id) -> Port:
        """
        Получить объект порта по его ID

        Args:
            id (str): Идентификатор порта

        Returns:
            object: Возвращает объект порта :class:`rcp.api.Port`
        """
        return Port().retrieve(id)

    @classmethod
    def port_create(cls, network: Network or str, ip_address: str = '0.0.0.0',
                    wait: bool = True, timeout='default', **kwargs) -> Port:
        """
        Создать объект

        Args:
            ip_address (str): ip адрес
            network (object, str): Объект класса :class:`rcp.api.Network` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Port`
        """
        return Port().create(ip_address=ip_address, network=network,
                             wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def port_create_fip(cls, vdc: Vdc or str, wait: bool = True, timeout='default', **kwargs) -> Port:
        """
        Получить публичный ip адрес во ВЦОД

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Port`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Port().create_fip(vdc=vdc, wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def port_update(cls, port: Port or str, wait: bool = True, timeout='default', **kwargs) -> Port:
        """
        Сохранить изменения

        Args:
            port(object, str): Объект класса :class:`rcp.api.Port` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Port`
        """
        if type(port) is str:
            port = Port().retrieve(id=port)
        return port.update(wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def port_connect(cls, port: Port or str, vm: Vm or str = None, router: Router or str = None,
                     wait: bool = True, timeout='default') -> Port:
        """
        Подключить порт к устройству

        Args:
            port(object, str): Объект класса :class:`rcp.api.Port` или его id
            vm(object, str): Объект класса :class:`rcp.api.Vm` или его id
            router(object, str): Объект класса :class:`rcp.api.Router` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Если производится попытка присоединить
                           несуществующий объект

            PortAlreadyConnected: Если производится попытка
                                  присоединить уже присоединенный порт

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Port`
        """
        if vm is not None and type(vm) is str:
            vm = Vm().retrieve(id=vm)
        elif router is not None and type(router) is str:
            router = Router().retrieve(id=router)
        if type(port) is str:
            port = Port().retrieve(id=port)
        return port.connect(vm=vm, router=router, wait=wait, timeout=timeout)

    @classmethod
    def port_disconnect(cls, port: Port or str, wait: bool = True, timeout='default') -> Port:
        """
        Отключить порт

        Args:
            port(object, str): Объект класса :class:`rcp.api.Port` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Port`
        """
        if type(port) is str:
            port = Port().retrieve(id=port)
        return port.disconnect(wait=wait, timeout=timeout)

    @classmethod
    def port_delete(cls, port: Port or str, wait: bool = True, timeout='default'):
        """
        Удалить порт

        Args:
            port(object, str): Объект класса :class:`rcp.api.Port` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if type(port) is str:
            port = Port().retrieve(id=port)
        port.delete(wait=wait, timeout=timeout)

    @classmethod
    def port_force_delete(cls, port: Port or str, wait: bool = True, timeout='default'):
        """
        Удалить порт, даже если он подключен к сущности

        Args:
            port(object, str): Объект класса :class:`rcp.api.Port` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if type(port) is str:
            port = Port().retrieve(id=port)
        port.force_delete(wait=wait, timeout=timeout)
