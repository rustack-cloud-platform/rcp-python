from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId
from esu.consts import DEFAULT_TIMEOUT, IMAGE_CREATE_TIMEOUT, \
    IMAGE_DEPLOY_TIMEOUT
from esu.vm import Vm


class File(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        size (str): Размер файла
        type (str): Тип файла
    """
    class Meta:
        id = Field()
        name = Field()
        type = Field()
        size = Field()


class Image(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        files (list): Список объектов класса :class:`esu.File`. Список файлов в
                        образе
        size (str): Размер образа
        type (str): Тип образа
        vdc (object): Объект класса :class:`esu.Vdc`. ВЦОД, к которому
                      относится образ
    """
    class Meta:
        files = FieldList(File, allow_none=True)
        id = Field()
        name = Field()
        size = Field()
        type = Field()
        vdc = Field('esu.Vdc')

    @classmethod
    def get_object(cls, id):
        """
        Получить объект образа по его ID

        Args:
            id (str): Идентификатор образа

        Returns:
            object: Возвращает объект образа :class:`esu.Image`
        """
        image = cls(id=id)
        image._get_object('v1/image', image.id)

        return image

    def create_from_vm(self, vm):
        """
        Создать образ из существующего сервера

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit(vm=vm, wait_time=IMAGE_CREATE_TIMEOUT)

    def create_for_upload(self):
        """
        Создать объект образа для последующей загрузки в него файлов

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        self._commit()

    def get_upload_link(self):
        """
        Получить ссылку для загрузки файлов образа
        """
        image = {'name': self.name, 'type': self.type}

        resp = self._call('POST', 'v1/image/{}/file'.format(self.id), **image)
        url = '{}{}'.format(BaseAPI.endpoint_url, resp['url'])
        return url

    def commit_upload(self):
        """
        Подтвердить окончание загрузки файлов образа.
        Подтверждение необходимо после загрузки файлов образа по полученному
        url для загрузки файлов
        """
        resp = self._call('POST', 'v1/image/{}/commit'.format(self.id))
        self.kwargs = resp
        self._fill()
        return self

    def save(self):
        """
        Сохранить изменения
        """
        if self.id is None:
            raise ObjectHasNoId

        self._commit()
        return self

    def _commit(self, vm=None, wait_time=DEFAULT_TIMEOUT):
        image = {'vdc': self.vdc.id, 'name': self.name}
        if vm is not None:
            image['vm'] = vm.id
        else:
            image['type'] = self.type
        self._commit_object('v1/image', wait_time, **image)

    def destroy(self):
        """
        Удалить объект образа

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/image', self.id)
        self.id = None

    def get_download_link(self, file):
        """
        Получить ссылку для скачивания файла образа
        """
        resp = self._call('GET',
                          'v1/image/{}/file/{}'.format(self.id, file.id))
        url = '{}{}'.format(self.endpoint_url, resp['url'])
        return url

    def deploy_vm_from_image(self, vm):
        """
        Создать сервер из образа

        Args:
            vm (object) - объект создаваемого сервера :class:`esu.Vm`

        Returns:
            object: объект созданного из образа сервера  :class:`esu.Vm`
        """

        vm = {
            'vdc': vm.vdc.id,
            'name': vm.name,
            'cpu': vm.cpu,
            'ram': vm.ram,
            'network': vm.ports[0].network.id,
            'storage_profile': vm.disks[0].storage_profile.id
        }

        resp = self._call('POST', 'v1/image/{}/deploy'.format(self.id),
                          wait_time=IMAGE_DEPLOY_TIMEOUT, **vm)
        vm = Vm.get_object(id=resp['id'])
        return vm
