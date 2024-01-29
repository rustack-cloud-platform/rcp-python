from .base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId, PortAlreadyConnected
from rcp.api.consts import PORT_ENDPOINT


class ConnectedObject(BaseAPI):
    """
    Args:
        id (str): Идентификатор подключённого объекта
        type (object): Тип объекта
        name (object): Имя подключённого объекта
        vdc (str): Объект :class:`rcp.api.Vdc`
    """
    class Meta:
        id = Field(allow_none=True)
        type = Field()
        name = Field()
        vdc = Field('rcp.api.Vdc', allow_none=True)


class Port(BaseAPI):
    """
    Args:
        id (str): Идентификатор порта
        ip_address (str): IP адрес
        type (str): Тип
        vdc (object): Объект класса :class:`rcp.api.Vdc`. ВЦОД, к которому
                      относится данный виртуальный сервер
        fw_templates (list): Включенные шаблоны брандмауэра
                             :class:`rcp.api.FirewallTemplate`
        network (object): Сеть :class:`rcp.api.Network`

    .. note:: Поле ``network`` необходимо для создания в качестве подключения
              к приватной сети ВЦОД.

              Поля ``ip_address`` и ``fw_templates`` опциональны при создании
              подключения к приватной сети ВЦОД

              Поля ``ip_address`` и ``fw_templates`` могут быть изменены для
              существующего объекта

              При создании подключения плавающего IP обязательных полей нет
    """
    class Meta:
        id = Field()
        ip_address = Field()
        type = Field()
        vdc = Field("rcp.api.Vdc", allow_none=True)
        fw_templates = FieldList('rcp.api.FirewallTemplate', allow_none=True)
        network = Field('rcp.api.Network')
        connected = Field(ConnectedObject, allow_none=True)
        vm = Field('rcp.api.Vm')
        router = Field('rcp.api.Router', allow_none=True)
        tags = FieldList('rcp.api.Tag')

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект порта по его ID

        Args:
            id (str): Идентификатор порта

        Returns:
            object: Возвращает объект порта :class:`rcp.api.Port`
        """
        port = cls(id=id)
        port._get_object(PORT_ENDPOINT, port.id)
        return port

    def create_fip(self, vdc, wait, timeout, **kwargs):
        """
        Создать объект

        Returns:
            object: Возвращает объект порта :class:`rcp.api.Port`
        """
        # port = {'vdc': vdc.id}
        port = {}
        for k in self.__dict__:
            if k in locals():
                v = locals()[k]
                if isinstance(v, BaseAPI):
                    port[k] = v.id
                elif (isinstance(v, str) or isinstance(v, int) or v is None or
                      not isinstance(v, dict)):
                    port[k] = v
                elif isinstance(v, dict):
                    for k1 in v:
                        port[k1] = v[k1]
        self._commit_object(PORT_ENDPOINT, wait=wait, timeout=timeout, **port)
        return self

    def create(self, network, wait, timeout, ip_address='0.0.0.0', **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId
        port = {}
        for k in self.__dict__:
            if k in locals():
                v = locals()[k]
                if isinstance(v, BaseAPI):
                    port[k] = v.id
                elif (isinstance(v, str) or isinstance(v, int) or v is None or
                      not isinstance(v, dict)):
                    port[k] = v
                elif isinstance(v, dict):
                    for k1 in v:
                        port[k1] = v[k1]
        self._commit_object(PORT_ENDPOINT, wait=wait, timeout=timeout, **port)
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

        port = {}
        for k in self.__dict__:
            if k.startswith('_') or k != 'Vm':
                continue
            v = self.__dict__[k]
            if isinstance(v, BaseAPI):
                port[k] = v.id
            elif isinstance(v, str) or isinstance(v, int) or v is None:
                port[k] = v
            elif not isinstance(v, dict):
                port[k] = [v2.name for v2 in v or []]
        for k, v in kwargs.items():
            port[k] = v
        self._commit_object(PORT_ENDPOINT, wait=wait, timeout=timeout, **port)
        return self

    # def _commit(self):
    #     port = {
    #         'ip_address': self.ip_address or '0.0.0.0',
    #         'fw_templates': [o.id for o in self.fw_templates or []]
    #     }
    #
    #     if self.id is None:
    #         port['network'] = self.network.id
    #         if self.vm is not None:
    #             port['vm'] = self.vm.id
    #         elif self.router is not None:
    #             port['router'] = self.router.id
    #
    #     self._commit_object('v1/port', **port)

    def connect(self, vm, router, wait, timeout):
        """
        Подключить

        Raises:
            ObjectHasNoId: Если производится попытка присоединить
                           несуществующий объект

            PortAlreadyConnected: Если производится попытка
                                  присоединить уже присоединенный порт
        """
        if self.id is None:
            raise ObjectHasNoId

        if self.connected is not None:
            raise PortAlreadyConnected

        port = {}
        if vm is not None:
            port = {'vm': vm.id}
        elif router is not None:
            port = {'router': router.id}

        self._commit_object(PORT_ENDPOINT, wait=wait, timeout=timeout, **port)
        return self

    def disconnect(self, wait, timeout):
        """
        Отключить порт

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._call('PATCH', '{}/{}/disconnect'.format(PORT_ENDPOINT, self.id),
                   wait=wait, timeout=timeout)
        self._fill()
        self.connected = None
        self.vm = None
        self.router = None
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

        self._destroy_object(PORT_ENDPOINT, self.id, wait=wait, timeout=timeout)
        self.id = None

    def force_delete(self):
        """
        Удалить объект, даже если он подключен к сущности

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._call('DELETE', '{}/{}/force'.format(PORT_ENDPOINT, self.id))
        self.id = None
