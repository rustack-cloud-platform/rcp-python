from rcp.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId
from rcp.consts import DEFAULT_TIMEOUT, SNAPSHOT_TIMEOUT, VM_CREATE_TIMEOUT


class Vm(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        description (str): Описание. Любой произвольный пользовательский текст
        cpu (int): Количество ядер
        ram (int): Количество ОЗУ в ГБ
        power (bool): Текущее состояние питания. Включен или выключен
        vdc (object): Объект класса :class:`rcp.Vdc`. ВЦОД, к которому
                      относится данный виртуальный сервер
        template (object): Объект класса :class:`rcp.Template`. Шаблон
                           операционной системы
        metadata (list): Список объектов класса :class:`rcp.VmMetadata`.
                         Список полей, необходимых для создания виртуального
                         выделенного сервера. Например, пароль или имя
                         пользователя.
        ports (list): Список объектов класса :class:`rcp.Port`. Список сетей,
                      к которым подключен данный виртуальный сервер
        disks (list): Список объектов класса :class:`rcp.Disk`. Список дисков,
                      подключенных к данному виртуальному серверу
        floating (object): Объект класса :class:`rcp.Port`. Порт подключения
                           виртаульаного выделенного сервера к внешней сети.
                           Если None, сервер не имеет подключения к внешней
                           сети.

    .. note:: Поля ``name``, ``cpu``, ``ram``, ``template``, ``ports``,
              ``disks`` и ``vdc`` необходимы для создания.

              Поля ``metadata``, ``description`` и ``floating`` опциональны
              при создании.

              Поля ``name``, ``description``, ``cpu``, ``ram``, ``floating``
              могут быть изменены для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        description = Field()
        cpu = Field()
        ram = Field()
        power = Field()
        vdc = Field('rcp.Vdc')
        template = Field('rcp.Template')
        metadata = FieldList('rcp.VmMetadata')
        ports = FieldList('rcp.Port')
        disks = FieldList('rcp.Disk')
        floating = Field('rcp.Port', allow_none=True)
        hotadd_feature = Field()
        cdrom = Field('rcp.Image', allow_none=True)

    @classmethod
    def get_object(cls, id):
        """
        Получить объект виртуального сервера по его ID

        Args:
            id (str): Идентификатор виртуального сервера

        Returns:
            object: Возвращает объект виртуального сервера :class:`rcp.Vm`
        """
        vm = cls(id=id)
        vm._get_object('v1/vm', vm.id)
        for disk in vm.disks:
            disk.vm = vm

        return vm

    def create(self, name: str, vdc, template, cpu: int, ram, ports,
               disks, metadata, floating=None,
               description: str = None, hotadd_feature=None,
               **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        vm = {
            'name': name,
            'vdc': vdc.id,
            'template': template.id,
            'cpu': cpu,
            'ram': ram,
            'ports': [{
                'id': o.id,
            } if o.id else {
                'network': o.network.id,
                'fw_templates': [o2.id for o2 in o.fw_templates or []]
            } for o in ports],
            'disks': [{
                'name': o.name,
                'size': o.size,
                'storage_profile': o.storage_profile.id
            } for o in disks],
            'metadata': [{
                'field': o.field.id,
                'value': o.value
            } for o in metadata],
            'description': description or ''
        }
        if floating:
            # keep/change or get a new IP
            floating = floating.id or '0.0.0.0'
        vm['floating'] = floating
        if hotadd_feature:
            vm['hotadd_feature'] = True
        self._commit_object('v1/vm', **vm, **kwargs)
        return self

    def update(self, name: str=None, cpu: int=None, ram=None, ports=None, disks=None, floating=None,
               hotadd_feature=None, description: str = None, **kwargs):
        """
        Сохранить изменения
        """
        if self.id is None:
            raise ObjectHasNoId
        vm = {
            'name': name or self.name,
            'cpu': cpu or self.cpu,
            'ram': ram or self.ram,
            'ports': [{
                'id': o.id,
            } if o.id else {
                'network': o.network.id,
                'fw_templates': [o2.id for o2 in o.fw_templates or []]
            } for o in ports or self.ports],
            'disks': [{
                'name': o.name,
                'size': o.size,
                'storage_profile': o.storage_profile.id
            } for o in disks or self.disks],
            'description': description or ''
        }
        if floating:
            # keep/change or get a new IP
            floating = floating.id or '0.0.0.0'
        vm['floating'] = floating
        if hotadd_feature:
            vm['hotadd_feature'] = True
        self._commit_object('v1/vm', VM_CREATE_TIMEOUT, **vm, **kwargs)
        return self

    # def _commit(self, wait_time=DEFAULT_TIMEOUT):
    #     vm = {
    #         'vdc': self.vdc.id,
    #         'template': self.template.id,
    #         'name': self.name,
    #         'cpu': self.cpu,
    #         'ram': self.ram,
    #         'description': self.description or '',
    #         'ports': [{
    #             'id': o.id,
    #         } if o.id else {
    #             'network': o.network.id,
    #             'fw_templates': [o2.id for o2 in o.fw_templates or []]
    #         } for o in self.ports],
    #         'disks': [{
    #             'name': o.name,
    #             'size': o.size,
    #             'storage_profile': o.storage_profile.id
    #         } for o in self.disks]
    #     }
    #
    #     if self.id is None:
    #         vm['metadata'] = [{
    #             'field': o.field.id,
    #             'value': o.value
    #         } for o in self.metadata]
    #
    #     floating = None
    #     if self.floating:
    #         # keep/change or get a new IP
    #         floating = self.floating.id or '0.0.0.0'
    #     vm['floating'] = floating
    #
    #     if self.hotadd_feature:
    #         vm['hotadd_feature'] = True
    #
    #     self._commit_object('v1/vm', wait_time, **vm)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/vm', self.id)
        self.id = None

    def add_disk(self, disk):
        """
        Создать и присоединить к виртуальному серверу новый диск

        Args:
            disk (object): Объект диска :class:`rcp.Disk`
        """
        if disk.id:
            raise ValueError('You must pass a new Disk object')
        disk.vm = self
        disk._commit()
        self.disks.append(disk)

    def attach_disk(self, disk):
        """
        Присоединить существующий во ВЦОДе диск к виртуальному серверу

        Args:
            disk (object): Объект диска :class:`rcp.Disk`
        """
        if not disk.id:
            raise ValueError('Disk is not exists')

        if disk.vm is not None:
            raise ValueError('Disk must be unattached')

        disk.vm = self
        disk.save()
        self.disks.append(disk)

    def detach_disk(self, disk):
        """
        Отсоединить диск от виртуального сервера

        Args:
            disk (object): Объект диска :class:`rcp.Disk`
        """
        self._call('POST', 'v1/disk/{}/detach'.format(disk.id))
        disk.vm = None
        self.disks = [d for d in self.disks if d.id != disk.id]

    def add_port(self, port):
        """
        Добавить подключение

        Args:
            port (object): Новый объект :class:`rcp.Port`
        """
        port = self._call('POST', 'v1/port', vm=self.id,
                          network=port.network.id)
        self.ports.append(port)
        self._fill()

    def remove_port(self, port):
        """
        Удалить подключение

        Args:
            port (object): Существующий объект :class:`rcp.Port`
        """
        self._call('DELETE', 'v1/port/{}'.format(port.id))
        self.ports = [o for o in self.ports if o.id != port.id]

    def power_on(self):
        """
        Включить виртуальный сервер
        """
        self._call('POST', 'v1/vm/{}/state'.format(self.id), state='power_on')
        self.power = True

    def power_off(self):
        """
        Выключить виртуальный сервер
        """
        self._call('POST', 'v1/vm/{}/state'.format(self.id), state='power_off')
        self.power = False

    def reboot(self):
        """
        Перезагрузить виртуальный сервер
        """
        self._call('POST', 'v1/vm/{}/state'.format(self.id), state='reboot')

    def get_vnc_url(self):
        """
        Получить ссылку на VNC для открытия консоли управления сервером

        Returns:
            str: Адрес VNC консоли
        """
        vnc = self._call('POST', 'v1/vm/{}/vnc'.format(self.id))
        uri = vnc['url']
        return '{}{}'.format(self.endpoint_url, uri)

    def revert(self, snapshot):
        """
        Восстановить сервер из снапшота

        Args:
            snapshot (object): объект снапшота :class:`rcp.Snapshot`
        """
        vm = self._call('POST', 'v2/snapshot/{}/revert'.format(snapshot.id),
                        wait_time=SNAPSHOT_TIMEOUT)
        return vm

    def mount_iso(self, image):
        """
        Примонтировать iso к серверу как CD-ROM.
        После перезагрузки сервера он будет загружен с этого
        диска если он загрузочный

        Args:
            image (object): объект образа :class:`rcp.Image`
        """
        image = {'image': image.id}
        self._call('POST', 'v1/vm/{}/mount_iso'.format(self.id), **image)

    def unmount_iso(self):
        """
        Отмонтировать iso от сервера
        После перезагрузки сервера он будет загружен с основного диска
        """
        self._call('POST', 'v1/vm/{}/unmount_iso'.format(self.id))
