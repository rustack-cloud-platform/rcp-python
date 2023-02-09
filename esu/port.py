from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId


class Port(BaseAPI):
    """
    Args:
        id (str): Идентификатор порта
        ip_address (str): IP адрес
        type (str): Тип
        vdc (object): Объект класса :class:`esu.Vdc`. ВЦОД, к которому
                      относится данный виртуальный сервер
        fw_templates (list): Включенные шаблоны брандмауэра
                             :class:`esu.FirewallTemplate`
        network (object): Сеть :class:`esu.Network`

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
        vdc = Field("esu.Vdc")
        fw_templates = FieldList('esu.FirewallTemplate')
        network = Field('esu.Network')
        device = Field()

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект порта по его ID

        Args:
            id (str): Идентификатор порта
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект порта :class:`esu.Port`
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
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект порта :class:`esu.Port`
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

    #pylint: disable=import-outside-toplevel
    def _commit(self):
        from esu import Router, Vm

        port = {
            'ip_address': self.ip_address or '0.0.0.0',
            'network': self.network.id,
        }
        if isinstance(self.device, Vm):
            port['vm'] = self.device.id
            port['fw_templates'] = [o.id for o in self.fw_templates or []]
        elif isinstance(self.device, Router):
            port['router'] = self.device.id

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
        self.device = None
        self._fill()

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
