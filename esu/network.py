from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId, resolve


class Network(BaseAPI):
    """
    Args:
        id (str): Идентификатор сети
        name (str): Имя сети
        vdc (object): Объект класса :class:`esu.Vdc`. ВЦОД, к которому
                      относится сеть
        is_default (bool): True для сети по умолчанию
        subnets (object): Список объектов класса :class:`esu.Subnet`
        mtu (int): MTU сети

    .. note:: Поля ``name`` и ``vdc`` необходимы для создания.

              Поле ``subnets`` опционально при создании.

              Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('esu.Vdc', allow_none=True)
        is_default = Field()
        subnets = FieldList('esu.Subnet')
        mtu = Field()

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект сети по его ID

        Args:
            id (str): Идентификатор сети
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект сети :class:`esu.Network`
        """
        network = cls(token=token, id=id)
        network._get_object('v1/network', network.id)
        return network

    def create(self):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        subnets = self.subnets or []
        if self.vdc.hypervisor.type == 'vmware':
            self.mtu = 1500
        self._commit()

        for subnet in subnets:
            self.add_subnet(subnet)

    def save(self):
        """
        Сохранить изменения

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._commit()

    def _commit(self):
        return self._commit_object('v1/network', vdc=self.vdc.id,
                                   name=self.name, mtu=self.mtu)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/network', self.id)
        self.id = None

    def add_subnet(self, subnet):
        """
        Добавить подсеть

        Args:
            subnet (object): Объект подсети :class:`esu.Subnet`
        """
        if subnet.id:
            raise ValueError('You must pass a new Subnet object')

        subnet = self._call('POST', 'v1/network/{}/subnet'.format(self.id),
                            cidr=subnet.cidr, gateway=subnet.gateway,
                            start_ip=subnet.start_ip, end_ip=subnet.end_ip,
                            enable_dhcp=subnet.enable_dhcp, subnet_routes=[],
                            dns_servers=[])
        self.subnets.append(resolve('esu.Subnet')(token=self.token, **subnet))

    def remove_subnet(self, subnet):
        """
        Удалить подсеть

        Args:
            subnet (object): Объект подсети :class:`esu.Subnet`
        """
        self._call('DELETE',
                   'v1/network/{}/subnet/{}'.format(self.id, subnet.id))
        self.subnets = [s for s in self.subnets if s.id != subnet.id]
