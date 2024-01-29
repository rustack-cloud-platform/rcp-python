from .backup import Backup
from .base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from .disk import Disk
from .firewall_template import FirewallTemplate
from .hypervisor import Hypervisor
from .image import Image
from .kubernetes_template import KubernetesTemplate
from .port import Port
from .storage_profile import StorageProfile
from .template import Template
from .vm import Vm
from .vm_metadata import VmMetadata
from .consts import VDC_ENDPOINT


class Vdc(BaseAPI):
    """
    Args:
        id (str): Идентификатор ВЦОД
        name (str): Имя ВЦОД
        hypervisor (object): Объект класса :class:`rcp.api.Hypervisor`
        project (object): Объект класса :class:`rcp.api.Project`. Проект, к
                          которому относится данный ВЦОД

    .. note:: Поля ``name``, ``hypervisor`` и ``project`` необходимы для
              создания.

              Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        hypervisor = Field('rcp.api.Hypervisor')
        project = Field('rcp.api.Project')
        tags = Field()

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект ВЦОД по его ID

        Args:
            id (str): Идентификатор ВЦОД

        Returns:
            object: Возвращает объект ВЦОД :class:`rcp.api.Vdc`
        """
        vdc = cls(id=id)
        vdc._get_object(VDC_ENDPOINT, vdc.id)
        return vdc

    def create(self, name: str, project, hypervisor: Hypervisor or str, wait, timeout, **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit_object(VDC_ENDPOINT, project=project.id, name=name,
                            hypervisor=hypervisor.id, wait=wait, timeout=timeout, **kwargs)
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
        vdc = {
            'name': self.name,
            'tags': [tag.get('name') for tag in self.tags]
        }
        for k, v in kwargs.items():
            vdc[k] = v
        self._commit_object(VDC_ENDPOINT, wait=wait, timeout=timeout, **vdc)
        return self

    def delete(self, wait, timeout):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(VDC_ENDPOINT, self.id, wait=wait, timeout=timeout)
        self.id = None

    # TODO will move to vdc_mixin
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
