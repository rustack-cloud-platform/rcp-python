from .base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId
from rcp.api.consts import DISK_ENDPOINT


class Disk(BaseAPI):
    """
    Args:
        id (str): Идентификатор диска
        name (str): Имя диска
        size (int): Размер диска (ГБ)
        scsi (str): Порт, к которому подключен диск
        vm (object): Объект виртуального сервера :class:`rcp.api.Vm`
        storage_profile (object): Объект :class:`rcp.api.StorageProfile`

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
        vdc = Field('rcp.api.Vdc')
        vm = Field('rcp.api.Vm', allow_none=True)
        storage_profile = Field('rcp.api.StorageProfile')
        tags = FieldList('rcp.api.Tag')

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект диска по его ID

        Args:
            id (str): Идентификатор диска

        Returns:
            object: Возвращает объект диска :class:`rcp.api.Disk`
        """
        disk = cls(id=id)
        disk._get_object(DISK_ENDPOINT, disk.id)
        return disk

    def create(self, name: str, size: int, storage_profile, vdc, wait, timeout, **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId
        disk = {}
        for k in self.__dict__:
            if k in locals():
                v = locals()[k]
                if isinstance(v, BaseAPI):
                    disk[k] = v.id
                elif (isinstance(v, str) or isinstance(v, int) or v is None or
                      not isinstance(v, dict)):
                    disk[k] = v
                elif isinstance(v, dict):
                    for k1 in v:
                        disk[k1] = v[k1]
        self._commit_object(DISK_ENDPOINT, wait=wait, timeout=timeout, **disk)
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
        disk = {}
        for k in self.__dict__:
            if k.startswith('_'):
                continue
            v = self.__dict__[k]
            if isinstance(v, BaseAPI):
                disk[k] = v.id
            elif isinstance(v, str) or isinstance(v, int) or v is None:
                disk[k] = v
            elif not isinstance(v, dict):
                disk[k] = [v2.name for v2 in v or []]
        for k, v in kwargs.items():
            disk[k] = v
        self._commit_object(DISK_ENDPOINT, wait=wait, timeout=timeout, **disk)
        return self

    def attach(self, vm, wait, timeout):
        """
        Присоединить существующий во ВЦОДе диск к виртуальному серверу
        """
        if not self.id:
            raise ValueError('Disk is not exists')

        if self.vm is not None:
            raise ValueError('Disk must be unattached')

        self._call('POST', DISK_ENDPOINT.format(self.id), vm=vm.id, wait=wait, timeout=timeout)
        self.vm = vm
        self._fill()

    def detach(self, wait, timeout):
        """
        Отсоединить диск от виртуального сервера
        """
        self._call('POST', '{}/{}/detach'.format(DISK_ENDPOINT, self.id),
                   wait=wait, timeout=timeout)
        self.vm = None

    def delete(self, wait, timeout):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(DISK_ENDPOINT, self.id, wait=wait, timeout=timeout)
        self.id = None
