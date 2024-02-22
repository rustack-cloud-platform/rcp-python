from esu.backup import Backup
from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from esu.disk import Disk
from esu.firewall_template import FirewallTemplate
from esu.image import Image
from esu.kubernetes_template import KubernetesTemplate
from esu.port import Port
from esu.storage_profile import StorageProfile
from esu.template import Template
from esu.vm import Vm
from esu.vm_metadata import VmMetadata


class Vdc(BaseAPI):
    """
    Args:
        id (str): Идентификатор ВЦОД
        name (str): Имя ВЦОД
        hypervisor (object): Объект класса :class:`esu.Hypervisor`
        project (object): Объект класса :class:`esu.Project`. Проект, к
                          которому относится данный ВЦОД

    .. note:: Поля ``name``, ``hypervisor`` и ``project`` необходимы для
              создания.

              Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        hypervisor = Field('esu.Hypervisor')
        project = Field('esu.Project')

    @classmethod
    def get_object(cls, id):
        """
        Получить объект ВЦОД по его ID

        Args:
            id (str): Идентификатор ВЦОД

        Returns:
            object: Возвращает объект ВЦОД :class:`esu.Vdc`
        """
        vdc = cls(id=id)
        vdc._get_object('v1/vdc', vdc.id)
        return vdc

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
        self._commit_object('v1/vdc', project=self.project.id, name=self.name,
                            hypervisor=self.hypervisor.id)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/vdc', self.id)
        self.id = None

    def get_vms(self):
        """
        Получить список виртуальных машин, доступных в рамках данного ВЦОД.

        Returns:
            list: Список объектов :class:`esu.Vm`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/vm', Vm, vdc=self.id)

    def get_templates(self):
        """
        Получить список шаблонов ОС для создания виртуальных машин, доступных
        в данном ВЦОДе.

        Returns:
            list: Список объектов: class:`esu.Template`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/template', Template, with_pages=False,
                              vdc=self.id)

    def get_storage_profiles(self):
        """
        Получить список профилей хранения, которые используются при добавлении
        дисков, доступных в данном ВЦОДе.

        Returns:
            list: Список объектов :class:`esu.StorageProfile`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/storage_profile', StorageProfile,
                              vdc=self.id)

    def get_firewall_templates(self):
        """
        Получить список шаблонов брандмауэра, доступных в данном ВЦОДе.

        Returns:
            list: Список объектов :class:`esu.FirewallTemplate`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/firewall', FirewallTemplate, vdc=self.id)

    def get_networks(self):
        """
        Получить список сетей, которые существуют в рамках данного ВЦОД.

        Returns:
            list: Список объектов :class:`esu.Network`
        """
        return self._get_list('v1/network', 'esu.Network', vdc=self.id)

    def get_routers(self):
        """
        Получить список маршрутизаторов, которые доступны в рамках данного
        ВЦОД.

        Returns:
            list: Список объектов :class:`esu.Router`
        """
        return self._get_list('v1/router', 'esu.Router', vdc=self.id)

    def get_ports(self):
        """
        Получить список подключений, которые существуют в данном ВЦОДе.

        Returns:
            list: Список объектов :class:`esu.Port`
        """
        return self._get_list('v1/port', 'esu.Port', vdc=self.id)

    def get_disks(self):
        """
        Получить список дисков, которые существуют в данном ВЦОДе.

        Returns:
            list: Список объектов :class:`esu.Disk`
        """
        return self._get_list('v1/disk', 'esu.Disk', vdc=self.id)

    def create_vm(self, name, template, password):  # helper
        """
        Быстрый способ создать виртуальный сервер в сети по-умолчанию и с
        настройками по-умолчанию.

        Args:
            name (str): Название нового виртуального сервера
            template (str): Название шаблона системы
            password (str): Пароль, который будет установлен на сервер
        """

        # pylint: disable=undefined-loop-variable
        for template_ in self.get_templates():
            if template_.name == template:
                break
        else:
            raise ValueError('Template not found')

        firewall = next(f for f in self.get_firewall_templates()
                        if f.id == '00000000-0000-0000-0000-000000000000')
        network = next(n for n in self.get_networks() if n.is_default)
        port = Port(network=network, fw_templates=[firewall])

        storage_profile = self.get_storage_profiles()[0]
        disk = Disk(name='Системный диск', size=template_.min_hdd,
                    storage_profile=storage_profile)

        metadata = []
        for field in template_.get_fields():
            value = field.default
            if field.system_alias == 'password':
                value = password
            metadata.append(VmMetadata(field=field, value=value))

        vm = Vm(name=name, cpu=template_.min_cpu, ram=template_.min_ram,
                vdc=self, template=template_, metadata=metadata, ports=[port],
                disks=[disk], token=self.token)
        vm.create()

        return vm

    def get_k8s_templates(self):
        """
        Получить список шаблонов k8s для создания кластеров, доступных
        в данном ВЦОДе.

        Returns:
            list: Список объектов :class:`esu.KubernetesTemplate`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/kubernetes_template', KubernetesTemplate,
                              vdc=self.id)

    def get_images(self):
        """
        Получить список образов, доступных в данном ВЦОДе.

        Returns:
            list: Список объектов :class:`esu.Image`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/image', Image, vdc=self.id)

    def get_backups(self):
        """
        Получить список задач резервного копирования, доступных в данном ВЦОДе.

        Returns:
            list: Список объектов :class:`esu.Backup`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/backup', Backup, vdc=self.id)
