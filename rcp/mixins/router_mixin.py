from rcp.api.consts import ROUTER_ENDPOINT, PORT_ENDPOINT, NETWORK_ENDPOINT
from rcp.api.router import Router
from rcp.api.network import Network
from rcp.api.subnet import Subnet
from rcp.api.vdc import Vdc
from rcp.api.port import Port


class RouterMixin:

    @classmethod
    def router_retrieve(cls, id) -> Router:
        """
        Получить объект маршрутизатора по его ID

        Args:
            id (str): Идентификатор маршрутизатора

        Returns:
            object: Возвращает объект маршрутизатора :class:`rcp.api.Router`
        """
        return Router().retrieve(id)

    @classmethod
    def router_create(cls, name: str, vdc: Vdc or str, connections: list[Port] or list[Network] or list[str],
                      connect_type: str = 'port' or 'network', floating: Port or str = None,
                      wait: bool = True, timeout='default', **kwargs) -> Router:
        """
        Создать объект

        Args:
            name (str): Имя
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            connections (list): Список объектов класса :class:`rcp.api.Port`
                                или :class:`rcp.api.Network` или его id
            connect_type (str): Тип подключения
            floating (object, str): Объект класса :class:`rcp.api.Port` или его id.
                                    Публичный IP адрес. '0.0.0.0' для случайного адреса
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Router`
        """
        ports = []
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        if type(floating) is str:
            floating = Port().retrieve(id=floating)
        for con in connections:
            port = None



            if connect_type == 'port' and type(con) is str:
                port = Port().retrieve(id=con)
            elif connect_type == 'network' and type(con) is str:
                port = Network().retrieve(id=con)
            if type(con) is Network:
                port = Port().create(network=con, wait=wait, timeout=timeout)
                ports.append(port)
            elif type(con) is Port:
                ports.append(port)
        return Router().create(name=name, vdc=vdc, ports=ports, floating=floating,
                               wait=wait, timeout=timeout, **kwargs)

    # TODO coming soon
    @classmethod
    def router_update(cls, router: Router or str, name: str = None, floating: Port or str = None,
                      wait: bool = True, timeout='default', **kwargs) -> Router:
        """
        Сохранить изменения

        Args:
            router (object, str): Объект класса :class:`rcp.api.Router` или его id.
            name (str): Имя
            floating (object, str): Объект класса :class:`rcp.api.Port` или его id.
                                    Публичный IP адрес. '0.0.0.0' для случайного адреса
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Router`
        """
        ports = []
        if type(router) is str:
            router = Router().retrieve(id=router)
        if type(floating) is str:
            floating = Port().retrieve(id=floating)
        return router.update(wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def router_delete(cls, router: Router or str, wait: bool = True, timeout='default'):
        """
        Удалить объект

        Args:
            router (object, str): Объект класса :class:`rcp.api.Router` или его id.
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if type(router) is str:
            router = Router().retrieve(id=router)
        router.delete(wait=wait, timeout=timeout)

    @classmethod
    def router_add_connect(cls, router: Router or str,
                           connect: Port or Network or str,
                           wait: bool = True, timeout='default') -> Router:
        """
        Добавить подключение

        Args:
            router (object, str): Объект класса :class:`rcp.api.Router` или его id.
            connect (object, str): Объект класса :class:`rcp.api.Port`
                                    или :class:`rcp.api.Network` или его id.
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Router`
        """
        if type(router) is str:
            router = Router().retrieve(id=router)
        port = None
        if type(connect) is str:
            ports = Port().get_list(PORT_ENDPOINT, Port, vdc=router.vdc.id)
            for p in ports:
                if p.id == connect:
                    port = p
            if port is None:
                networks = Network().get_list(NETWORK_ENDPOINT, Network, vdc=router.vdc.id)
                for n in networks:
                    if n.id == connect:
                        network = n
                        port = Port().create(network=network, wait=wait, timeout=timeout)
        elif type(connect) is Network:
            port = Port().create(network=connect, wait=wait, timeout=timeout)
        elif type(connect) is Port:
            port = connect
        return router.add_port(port=port, wait=wait, timeout=timeout)

    @classmethod
    def router_delete_connect(cls, router: Router or str,
                              connect: Port or Network or str,
                              wait: bool = True, timeout='default') -> Router:
        """
        Удалить подключение

        Args:
            router (object, str): Объект класса :class:`rcp.api.Router` или его id.
            connect (object, str): Объект класса :class:`rcp.api.Port`
                                    или :class:`rcp.api.Network` или его id.
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Router`
        """
        if type(router) is str:
            router = Router().retrieve(id=router)
        port = None
        ports = Port().get_list(PORT_ENDPOINT, Port, vdc=router.vdc.id, router=router.id)
        if type(connect) is str:
            for p in ports:
                if p.id == connect or p.network.id == connect:
                    port = p
        elif type(connect) is Network:
            for p in ports:
                if p.network.id == connect.id:
                    port = p
        elif type(connect) is Port:
            port = connect
        return router.remove_port(port=port, wait=wait, timeout=timeout)
