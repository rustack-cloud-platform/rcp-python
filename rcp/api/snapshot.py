from .base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from .consts import SNAPSHOT_TIMEOUT


class Snapshot(BaseAPI):
    """
    Args:
        id (str): Идентификатор снапшота
        name (str): Имя снапшота
        description (str): описание для снапшота
        vm (object): Объект класса :class:`rcp.Vm`. Сервер, к которому
                      относится данный снапшот

    .. note:: Поле ``name`` и ``vm`` необходимо для создания

              Поля ``description`` опцональны при создании

              Поля ``name`` и ``description`` могут быть изменены для
              существующего объекта

    """
    class Meta:
        id = Field()
        name = Field()
        vm = Field("rcp.Vm")
        description = Field()

    @classmethod
    def get_object(cls, id):
        """
        Получить объект порта по его ID

        Args:
            id (str): Идентификатор снапшота

        Returns:
            object: Возвращает объект порта :class:`rcp.Port`
        """
        snapshot = cls(id=id)
        snapshot._get_object('v2/snapshot', snapshot.id)
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

    # pylint: disable=import-outside-toplevel
    def _commit(self):
        description = self.description or ''
        self._commit_object('v2/snapshot', wait_time=SNAPSHOT_TIMEOUT,
                            name=self.name, description=description,
                            vm=self.vm.id)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v2/snapshot', self.id,
                             wait_time=SNAPSHOT_TIMEOUT)
        self.id = None
