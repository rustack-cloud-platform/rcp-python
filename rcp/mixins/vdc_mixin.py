from rcp.api.consts import (VDC_ENDPOINT, VM_ENDPOINT, TEMPLATE_ENDPOINT,
                            STORAGE_PROFILE_ENDPOINT, FIREWALL_TEMPLATE_ENDPOINT,
                            NETWORK_ENDPOINT, ROUTER_ENDPOINT, PORT_ENDPOINT,
                            DISK_ENDPOINT, K8S_TEMPLATE_ENDPOINT, K8S_ENDPOINT,
                            IMAGE_ENDPOINT, BACKUP_ENDPOINT)
from rcp.api.vdc import Vdc
from rcp.api.project import Project
from rcp.api.hypervisor import Hypervisor
from rcp.api.vm import Vm
from rcp.api.disk import Disk
from rcp.api.firewall_template import FirewallTemplate
from rcp.api.image import Image
from rcp.api.kubernetes_template import KubernetesTemplate
from rcp.api.port import Port
from rcp.api.storage_profile import StorageProfile
from rcp.api.template import Template
from rcp.api.vm_metadata import VmMetadata
from rcp.api.backup import Backup
from rcp.api.network import Network
from rcp.api.router import Router
from rcp.api.kubernetes import Kubernetes


class VdcMixin:

    @classmethod
    def vdc_retrieve(cls, id: str) -> Vdc:
        """
        Получить объект ВЦОД по его ID

        Args:
            id (str): Идентификатор ВЦОД

        Returns:
            object: Возвращает объект ВЦОД :class:`rcp.api.Vdc`
        """
        return Vdc().retrieve(id)

    @classmethod
    def vdc_create(cls, name: str, project: Project or str,
                   hypervisor: Hypervisor or str,
                   wait: bool = True, timeout='default', **kwargs) -> Vdc:
        """
        Создать объект

        Args:
            name (str): Имя
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            hypervisor (object, str): Объект класса :class:`rcp.api.Hypervisor` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует

        Returns:
            object: Возвращает объект проекта :class:`rcp.api.Vdc`

        .. note:: Поля ``name``, ``hypervisor`` и ``project`` необходимы для
              создания.

              Поле ``name`` может быть изменено для существующего объекта.
        """
        return Vdc().create(name=name, project=project, hypervisor=hypervisor,
                            wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def vdc_update(cls, vdc: Vdc or str,
                   wait: bool = True, timeout='default', **kwargs) -> Vdc:
        """
        Сохранить изменения

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект

        Returns:
            object: Возвращает объект проекта :class:`rcp.api.Vdc`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return vdc.update(wait=wait, timeout=timeout, **kwargs)

    @classmethod
    def vdc_delete(cls, vdc: Vdc or str,
                   wait: bool = True, timeout='default'):
        """
        Удалить объект

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            wait (bool): Включение/отключение ожидания выполнения задачи
            timeout (integer): Время ожидания выполнения задачи

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        vdc.delete(wait=wait, timeout=timeout)

    @classmethod
    def vdc_list(cls, **filters) -> list[Vdc]:
        """
        Получить ВЦОДы доступные пользователю.
        Если ВЦОДы находятся в разных проекта список будет содержать их все
        Вернет список объектов :class:`rcp.api.Vdc`.

        Args:
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Vdc`
        """
        return Vdc().get_list(VDC_ENDPOINT, Vdc, **filters)

    @classmethod
    def vdc_vms_list(cls, vdc: Vdc or str, **filters) -> list[Vdc]:
        """
        Получить список виртуальных машин, доступных в рамках данного ВЦОД.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Vm`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(VM_ENDPOINT, Vm, vdc=vdc.id, **filters)

    @classmethod
    def vdc_templates_list(cls, vdc: Vdc or str, **filters) -> list[Template]:
        """
        Получить список шаблонов ОС для создания виртуальных машин, доступных
        в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов: class:`rcp.api.Template`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(TEMPLATE_ENDPOINT, Template, vdc=vdc.id, **filters)

    @classmethod
    def vdc_storage_profiles_list(cls, vdc: Vdc or str, **filters) -> list[StorageProfile]:
        """
        Получить список профилей хранения, которые используются при добавлении
        дисков, доступных в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.StorageProfile`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(STORAGE_PROFILE_ENDPOINT, StorageProfile, vdc=vdc.id, **filters)

    @classmethod
    def vdc_firewall_templates_list(cls, vdc: Vdc or str, **filters) -> list[FirewallTemplate]:
        """
        Получить список шаблонов брандмауэра, доступных в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.FirewallTemplate`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(FIREWALL_TEMPLATE_ENDPOINT, FirewallTemplate, vdc=vdc.id, **filters)

    @classmethod
    def vdc_networks_list(cls, vdc: Vdc or str, **filters) -> list[Network]:
        """
        Получить список сетей, которые существуют в рамках данного ВЦОД.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Network`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(NETWORK_ENDPOINT, Network, vdc=vdc.id, **filters)

    @classmethod
    def vdc_routers_list(cls, vdc: Vdc or str, **filters) -> list[Router]:
        """
        Получить список маршрутизаторов, которые доступны в рамках данного
        ВЦОД.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Router`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(ROUTER_ENDPOINT, Router, vdc=vdc.id, **filters)

    @classmethod
    def vdc_ports_list(cls, vdc: Vdc or str, **filters) -> list[Port]:
        """
        Получить список подключений, которые существуют в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Port`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(PORT_ENDPOINT, Port, vdc=vdc.id, **filters)

    @classmethod
    def vdc_disks_list(cls, vdc: Vdc or str, **filters) -> list[Disk]:
        """
        Получить список дисков, которые существуют в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Disk`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(DISK_ENDPOINT, Disk, vdc=vdc.id, **filters)

    @classmethod
    def vdc_k8S_templates_list(cls, vdc: Vdc or str, **filters) -> list[KubernetesTemplate]:
        """
        Получить список шаблонов k8s для создания кластеров, доступных
        в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.KubernetesTemplate`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(K8S_TEMPLATE_ENDPOINT, KubernetesTemplate, vdc=vdc.id, **filters)

    @classmethod
    def vdc_k8s_list(cls, vdc: Vdc or str, **filters) -> list[Kubernetes]:
        """
        Получить список кластеров k8s, в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Kubernetes`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(K8S_ENDPOINT, Kubernetes, vdc=vdc.id, **filters)

    @classmethod
    def vdc_images_list(cls, vdc: Vdc or str, **filters) -> list[Image]:
        """
        Получить список образов, доступных в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Image`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(IMAGE_ENDPOINT, Image, vdc=vdc.id, **filters)

    @classmethod
    def vdc_backups_list(cls, vdc: Vdc or str, **filters) -> list[Backup]:
        """
        Получить список задач резервного копирования, доступных в данном ВЦОДе.

        Args:
            vdc (object, str): Объект класса :class:`rcp.api.Vdc` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Backup`
        """
        if type(vdc) is str:
            vdc = Vdc().retrieve(id=vdc)
        return Vdc().get_list(BACKUP_ENDPOINT, Backup, vdc=vdc.id, **filters)

    # TODO coming soon
    @classmethod
    def vdc_create_simple_vm(cls):
        pass
