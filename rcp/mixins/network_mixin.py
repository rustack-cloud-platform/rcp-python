from rcp.api.network import Network
from rcp.api.subnet import Subnet


class NetworkMixin:

    @classmethod
    def network_retrieve(cls, id) -> Network:
        """
        Получить объект сети по его ID

        Args:
            id (str): Идентификатор сети

        Returns:
            object: Возвращает объект сети :class:`rcp.api.Network`
        """
        return Network().retrieve(id)

    @classmethod
    def network_create(cls, name: str, subnets: list[Subnet] or list[str] = None,
                       mtu: int = 0, wait: bool = True, timeout='default', **kwargs) -> Network:
        """
        Создать объект

        Args:
            name (str): Имя
            subnets (list): Список объектов класса :class:`rcp.api.Subnet` или его id
            mtu (integer): MTU
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Network`
        """
        # TODO добавить обработку случая, когда mtu не задается
        return Network().create(name=name, subnets=subnets, mtu=mtu, wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def network_update(cls, network: Network or str, wait: bool = True,
                       timeout='default', **kwargs) -> Network:
        """
        Сохранить изменения

        Args:
            network (object, str): Объект класса :class:`rcp.api.Network` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        Returns:
            object: Возвращает объект проекта :class:`rcp.api.Network`
        """
        if type(network) is str:
            network = Network().retrieve(id=network)
        return network.update(wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def network_delete(cls, network: Network or str, wait: bool = True,
                       timeout='default'):
        """
        Удалить объект

        Args:
            network (object, str): Объект класса :class:`rcp.api.Network` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if type(network) is str:
            network = Network().retrieve(id=network)
        network.delete(wait=wait, timeout=timeout)

    @classmethod
    def network_add_subnet(cls, network: Network or str, subnet: Subnet, wait: bool = True,
                           timeout='default') -> Network:
        """
        Добавить подсеть

        Args:
            network (object, str): Объект класса :class:`rcp.api.Network` или его id
            subnet (object): Объект подсети :class:`rcp.api.Subnet`
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
        """
        if type(network) is str:
            network = Network().retrieve(id=network)
        return network.add_subnet(subnet=subnet, wait=wait, timeout=timeout)

    @classmethod
    def network_delete_subnet(cls, network: Network or str, subnet: Subnet, wait: bool = True,
                              timeout='default') -> Network:
        """
        Добавить подсеть

        Args:
            network (object, str): Объект класса :class:`rcp.api.Network` или его id
            subnet (object): Объект подсети :class:`rcp.api.Subnet`
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
        """
        if type(network) is str:
            network = Network().retrieve(id=network)
        return network.delete_subnet(subnet=subnet, wait=wait, timeout=timeout)
