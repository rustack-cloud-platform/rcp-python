from bcc.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId, PortAlreadyConnected


class ConnectedObject(BaseAPI):
    """
    Args:
        id (str): Идентификатор подключённого объекта
        type (object): Тип объекта
        name (object): Имя подключённого объекта
        vdc (str): Объект :class:`bcc.Vdc`
    """
    class Meta:
        id = Field(allow_none=True)
        type = Field()
        name = Field()
        vdc = Field('bcc.Vdc', allow_none=True)


class Port(BaseAPI):
    """
    Args:
        id (str): Идентификатор порта
        ip_address (str): IP адрес
        type (str): Тип
        vdc (object): Объект класса :class:`bcc.Vdc`. ВЦОД, к которому
                      относится данный виртуальный сервер
        fw_templates (list): Включенные шаблоны брандмауэра
                             :class:`bcc.FirewallTemplate`
        network (object): Сеть :class:`bcc.Network`

    .. note:: Поле ``network`` необходимо для создания в качестве подключения
              к приватной сети ВЦОД.

              Поля ``ip_address`` и ``fw_templates`` опцональны при создании
              подключения к приватной сети ВЦОД

              Поля ``ip_address`` и ``fw_templates`` могут быть изменены для
              существующего объекта

              При создании подключения плавающего IP обязательных полей нет
    """
    class Meta:
        id = Field()
        ip_address = Field()
        type = Field()
        vdc = Field("bcc.Vdc", allow_none=True)
        fw_templates = FieldList('bcc.FirewallTemplate', allow_none=True)
        network = Field('bcc.Network')
        connected = Field(ConnectedObject, allow_none=True)
        vm = Field('bcc.Vm')
        router = Field('bcc.Router', allow_none=True)

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект порта по его ID

        Args:
            id (str): Идентификатор порта
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **BCC_API_TOKEN**

        Returns:
            object: Возвращает объект порта :class:`bcc.Port`
        """
        port = cls(token=token, id=id)
        port._get_object('v1/port', port.id)
        return port

    def create_fip(self):
        """
        Получить объект порта по его ID

        Args:
            id (str): Идентификатор порта
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **BCC_API_TOKEN**

        Returns:
            object: Возвращает объект порта :class:`bcc.Port`
        """
        port = {'vdc': self.vdc.id}
        self._commit_object('v1/port', **port)

    def create(self):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit()

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
        port = {
            'ip_address': self.ip_address or '0.0.0.0',
            'fw_templates': [o.id for o in self.fw_templates or []]
        }

        if self.id is None:
            port['network'] = self.network.id
            port['vdc'] = self.vdc.id if self.vdc else None
            if self.vm is not None:
                port['vm'] = self.vm.id
            elif self.router is not None:
                port['router'] = self.router.id

        self._commit_object('v1/port', **port)

    def connect(self):
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

        if self.vm is not None:
            port = {'vm': self.vm.id}
        elif self.router is not None:
            port = {'router': self.router.id}

        self._commit_object('v1/port', **port)

    def disconnect(self):
        """
        Отключить порт

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._call('PATCH', 'v1/port/{}/disconnect'.format(self.id))
        self._fill()
        self.connected = None
        self.vm = None
        self.router = None

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/port', self.id)
        self.id = None

    def force_destroy(self):
        """
        Удалить объект, даже если он подключен к сущности

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._call('DELETE', 'v1/port/{}/force'.format(self.id))
        self.id = None
