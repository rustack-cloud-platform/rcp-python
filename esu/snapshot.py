from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class Snapshot(BaseAPI):
    """
    Args:
        id (str): Идентификатор снапшота
        name (str): Имя снапшота
        description (str): описание для шаблона брандмауэра
        vm (object): Объект класса :class:`esu.Vm`. Сервер, к которому
                      относится данный снапшот

    .. note:: Поле ``name`` и ``vm`` необходимо для создания

              Поля ``description`` опцональны при создании

              Поля ``name`` и ``description`` могут быть изменены для
              существующего объекта

    """
    class Meta:
        id = Field()
        name = Field()
        vm = Field("esu.Vm")
        description = Field()

    @classmethod
    def get_object(cls, id, vm, token=None):
        """
        Получить объект порта по его ID

        Args:
            id (str): Идентификатор снапшота
            vm (str): Идентификатор vm
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект порта :class:`esu.Port`
        """
        snapshot = cls(token=token, id=id, vm=vm)
        snapshot._get_object('v1/vm/{}/snapshot'.format(snapshot.vm.id),
                             snapshot.id)
        return snapshot

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
        description = self.description or ''
        self._commit_object('v1/vm/{}/snapshot'.format(self.vm.id),
                            name=self.name, description=description)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/vm/{}/snapshot'.format(self.vm.id), self.id)
        self.id = None
