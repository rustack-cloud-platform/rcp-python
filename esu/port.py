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
        fw_templates = [o.id for o in self.fw_templates]
        self._commit_object('v1/port', ip_address=self.ip_address,
                            type=self.type, vdc=self.vdc,
                            fw_templates=fw_templates, network=self.network)

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
