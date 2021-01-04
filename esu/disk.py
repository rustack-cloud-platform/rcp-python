from esu.base import BaseAPI, Field, ObjectHasNoId


class Disk(BaseAPI):
    """
    Args:
        id (str): Идентификатор диска
        name (str): Имя диска
        size (int): Размер диска (ГБ)
        scsi (str): Порт, к которому подключен диск
        vm (object): Объект виртуального сервера :class:`esu.Vm`
        storage_profile (object): Объект :class:`esu.StorageProfile`

    .. note:: Поля ``name``, ``size``, ``storage_profile`` могут быть изменены
              для существующего объекта.

    .. warning:: ``storage_profile`` можно изменить только для дисков в
                 сегменте VMware когда диск подключен к виртуальному серверу.
    """
    class Meta:
        id = Field()
        name = Field()
        size = Field()
        scsi = Field()
        vm = Field('esu.Vm', allow_none=True)
        storage_profile = Field('esu.StorageProfile')

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект диска по его ID

        Args:
            id (str): Идентификатор диска
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект диска :class:`esu.Disk`
        """
        disk = cls(token=token, id=id)
        disk._get_object('v1/disk', disk.id)
        return disk

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
        self._commit_object('v1/disk', name=self.name, size=self.size,
                            storage_profile=self.storage_profile.id,
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

        self._destroy_object('v1/disk', self.id)
        self.id = None
