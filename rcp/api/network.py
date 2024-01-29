from .base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId, resolve
from rcp.api.consts import NETWORK_ENDPOINT


class Network(BaseAPI):
    """
    Args:
        id (str): Идентификатор сети
        name (str): Имя сети
        vdc (object): Объект класса :class:`rcp.api.Vdc`. ВЦОД, к которому
                      относится сеть
        is_default (bool): True для сети по умолчанию
        subnets (object): Список объектов класса :class:`rcp.api.Subnet`
        mtu (integer): MTU

    .. note:: Поля ``name`` и ``vdc`` необходимы для создания.

              Поле ``subnets`` опционально при создании.

              Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('rcp.api.Vdc', allow_none=True)
        is_default = Field()
        subnets = FieldList('rcp.api.Subnet')
        mtu = Field()
        tags = FieldList('rcp.api.Tag')

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект сети по его ID

        Args:
            id (str): Идентификатор сети

        Returns:
            object: Возвращает объект сети :class:`rcp.api.Network`
        """
        network = cls(id=id)
        network._get_object(NETWORK_ENDPOINT, network.id)
        return network

    def create(self, name: str, subnets, mtu, wait, timeout, vdc=None, **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        network = {}
        for k in self.__dict__:
            if k in locals() and k != 'subnets':
                v = locals()[k]
                if isinstance(v, BaseAPI):
                    network[k] = v.id
                elif (isinstance(v, str) or isinstance(v, int) or v is None or
                      not isinstance(v, dict)):
                    network[k] = v
                elif isinstance(v, dict):
                    for k1 in v:
                        network[k1] = v[k1]

        if subnets is None:
            subnets = []
        self._commit_object(NETWORK_ENDPOINT, wait=wait, timeout=timeout, **network)

        for subnet in subnets:
            self.add_subnet(subnet, wait=wait, timeout=timeout)
        return self

    def update(self, wait, timeout, **kwargs):
        """
        Сохранить изменения

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        if self.id is None:
            raise ObjectHasNoId
        network = {}
        for k in self.__dict__:
            if k.startswith('_') or k != 'Subnet':
                continue
            v = self.__dict__[k]
            if isinstance(v, BaseAPI):
                network[k] = v.id
            elif isinstance(v, str) or isinstance(v, int) or v is None:
                network[k] = v
            elif not isinstance(v, dict):
                network[k] = [v2.name for v2 in v or []]
        for k, v in kwargs.items():
            network[k] = v
        self._commit_object(NETWORK_ENDPOINT, wait=wait, timeout=timeout, **network)
        return self

    def delete(self, wait, timeout):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(NETWORK_ENDPOINT, self.id, wait=wait, timeout=timeout)
        self.id = None

    def add_subnet(self, subnet, wait, timeout):
        """
        Добавить подсеть

        Args:
            subnet (object): Объект подсети :class:`rcp.api.Subnet`
        """
        if subnet.id:
            raise ValueError('You must pass a new Subnet object')

        subnet = self._call('POST', '{}/{}/subnet'.format(NETWORK_ENDPOINT, self.id),
                            cidr=subnet.cidr, gateway=subnet.gateway,
                            start_ip=subnet.start_ip, end_ip=subnet.end_ip,
                            enable_dhcp=subnet.enable_dhcp, subnet_routes=[],
                            dns_servers=[], wait=wait, timeout=timeout)
        self.subnets.append(resolve('rcp.api.Subnet')(token=self.token, **subnet))

    def delete_subnet(self, subnet, wait, timeout):
        """
        Удалить подсеть

        Args:
            subnet (object): Объект подсети :class:`rcp.api.Subnet`
        """
        self._call('DELETE',
                   '{}/{}/subnet/{}'.format(NETWORK_ENDPOINT, self.id, subnet.id),
                   wait=wait, timeout=timeout)
        self.subnets = [s for s in self.subnets if s.id != subnet.id]
