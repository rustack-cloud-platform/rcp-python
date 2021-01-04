from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId


class Router(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        vdc (object): ВЦОД, к которому относится маршрутизатор :class:`esu.Vdc`
        is_default (bool): True для маршрутизатора по умолчанию
        floating (object): Порт подключения к внешней сети :class:`esu.Port`
        ports (list): Список подключений маршрутизатора

    .. note:: Поля ``name``, ``ports`` и ``vdc`` необходимы для создания.

              Поле ``floating`` опционально при создании.

              Поля ``name`` и ``floating`` могут быть изменены для
              существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('esu.Vdc')
        is_default = Field()
        floating = Field('esu.Port', allow_none=True)
        ports = FieldList('esu.Port')

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект маршрутизатора по его ID

        Args:
            id (str): Идентификатор маршрутизатора
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект маршрутизатора :class:`esu.Router`
        """
        router = cls(token=token, id=id)
        router._get_object('v1/router', router.id)
        return router

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
        ports = [{'network': o.network.id} for o in self.ports]
        floating = None
        if self.floating:
            # keep/change or get a new IP
            floating = self.floating.id or '0.0.0.0'

        return self._commit_object('v1/router', vdc=self.vdc.id,
                                   name=self.name, ports=ports,
                                   floating=floating)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/router', self.id)
        self.id = None

    def add_port(self, port):
        """
        Добавить подключение

        Args:
            port (object): Новый объект :class:`esu.Port`
        """
        port = self._call('POST', 'v1/port', router=self.id,
                          network=port.network.id)
        self.ports.append(port)

    def remove_port(self, port):
        """
        Удалить подключение

        Args:
            port (object): Существующий объект :class:`esu.Port`
        """
        self._call('DELETE', 'v1/port/{}'.format(port.id))
        self.ports = [o for o in self.ports if o.id != port.id]
