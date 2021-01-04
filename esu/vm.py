from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId


class Vm(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        description (str): Описание. Любой произвольный пользовательский текст
        cpu (int): Количество ядер
        ram (int): Количество ОЗУ в ГБ
        power (bool): Текущее состояние питания. Включен или выключен
        vdc (object): Объект класса :class:`esu.Vdc`. ВЦОД, к которому
                      относится данный виртуальный сервер
        template (object): Объект класса :class:`esu.Template`. Шаблон
                           операционной системы
        metadata (list): Список объектов класса :class:`esu.VmMetadata`.
                         Список полей, необходимых для создания виртуального
                         выделенного сервера. Например, пароль или имя
                         пользователя.
        ports (list): Список объектов класса :class:`esu.Port`. Список сетей,
                      к которым подключен данный виртуальный сервер
        disks (list): Список объектов класса :class:`esu.Disk`. Список дисков,
                      подключенных к данному виртуальному серверу
        floating (object): Объект класса :class:`esu.Port`. Порт подключения
                           виртаульаного выделенного сервера к внешней сети.
                           Если None, сервер не имеет подключения к внешней
                           сети.
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **ESU_API_TOKEN**

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
        vdc = Field('esu.Vdc')
        template = Field('esu.Template')
        metadata = FieldList('esu.VmMetadata')
        ports = FieldList('esu.Port')
        disks = FieldList('esu.Disk')
        floating = Field('esu.Port', allow_none=True)

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект виртуального сервера по его ID

        Args:
            id (str): Идентификатор виртуального сервера
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект виртуального сервера :class:`esu.Vm`
        """
        vm = cls(token=token, id=id)
        vm._get_object('v1/vm', vm.id)
        for disk in vm.disks:
            disk.vm = vm

        return vm

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
        """
        if self.id is None:
            raise ObjectHasNoId

        self._commit()
        return self

    def _commit(self):
        ports = [{
            'network': o.network.id,
            'fw_templates': [o2.id for o2 in o.fw_templates or []]
        } for o in self.ports]
        disks = [{
            'name': o.name,
            'size': o.size,
            'storage_profile': o.storage_profile.id
        } for o in self.disks]
        metadata = [{
            'field': o.field.id,
            'value': o.value
        } for o in self.metadata]

        floating = None
        if self.floating:
            # keep/change or get a new IP
            floating = self.floating.id or '0.0.0.0'

        self._commit_object('v1/vm', vdc=self.vdc.id,
                            template=self.template.id, name=self.name,
                            cpu=self.cpu, ram=self.ram, ports=ports,
                            description=self.description or '',
                            floating=floating, disks=disks, metadata=metadata)

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

    def power_on(self):
        """
        Включить виртуальный сервер
        """
        if self.power:
            raise ValueError('VM is already on')
        self._call('POST', 'v1/vm/{}/state'.format(self.id), state='power_on')
        self.power = True

    def power_off(self):
        """
        Выключить виртуальный сервер
        """
        if not self.power:
            raise ValueError('VM is already off')

        self._call('POST', 'v1/vm/{}/state'.format(self.id), state='power_off')
        self.power = False

    def reboot(self):
        """
        Перезагрузить виртуальный сервер
        """
        if not self.power:
            raise ValueError('VM must be on')

        self._call('POST', 'v1/vm/{}/state'.format(self.id), state='reboot')

    def add_disk(self, disk):
        """
        Создать и присоединить к виртуальному серверу новый диск

        Args:
            disk (object): Объект диска :class:`esu.Disk`
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
            disk (object): Объект диска :class:`esu.Disk`
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
            disk (object): Объект диска :class:`esu.Disk`
        """
        self._call('POST', 'v1/disk/{}/detach'.format(disk.id))
        disk.vm = None
        self.disks = [d for d in self.disks if d.id != disk.id]

    def add_port(self, port):
        """
        Добавить подключение

        Args:
            port (object): Новый объект :class:`esu.Port`
        """
        port = self._call('POST', 'v1/port', vm=self.id,
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

    def get_vnc_url(self):
        """
        Получить ссылку на VNC для открытия консоли управления сервером

        Returns:
            str: Адрес VNC консоли
        """
        vnc = self._call('POST', 'v1/vm/{}/vnc'.format(self.id))
        uri = vnc['url']
        return '{}{}'.format(self.endpoint_url, uri)
