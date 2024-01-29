from rcp.api.consts import (PROJECT_ENDPOINT, VDC_ENDPOINT, HYPERVISOR_ENDPOINT,
                            DNS_ENDPOINT, KUBERNETES_ENDPOINT, S3_ENDPOINT,
                            PAAS_TEMPLATE_ENDPOINT, PAAS_SERVICE_ENDPOINT)
from rcp.api.project import Project
from rcp.api.client import Client
from rcp.api.vdc import Vdc
from rcp.api.hypervisor import Hypervisor
from rcp.api.dns import Dns
from rcp.api.kubernetes import Kubernetes
from rcp.api.s3 import S3
from rcp.api.paas_template import PaasTemplate
from rcp.api.paas_service import PaasService


class ProjectMixin:

    @classmethod
    def project_retrieve(cls, id: str) -> Project:
        """
        Получить объект проекта по его ID

        Args:
            id (str): Идентификатор проекта

        Returns:
            object: Возвращает объект проекта :class:`rcp.api.Project`
        """
        return Project().retrieve(id)

    @classmethod
    def project_create(cls, name: str, client: Client or str, **kwargs) -> Project:
        """
        Создать объект

        Args:
            name (str): Имя
            client (object, str): Объект класса :class:`rcp.api.Client` или его id.
                                    Клиент, к которому относится проект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует

        Returns:
            object: Возвращает объект проекта :class:`rcp.api.Project`

        .. note:: Поля ``name`` и ``client`` необходимы для создания.
        """
        return Project().create(name=name, client=client, **kwargs)

    @classmethod
    def project_update(cls, project: Project or str, **kwargs) -> Project:
        """
        Сохранить изменения
        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            kwargs (**kwargs): Список параметров ключ=значение

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект

        Returns:
            object: Возвращает объект проекта :class:`rcp.api.Project`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.update(**kwargs)

    @classmethod
    def project_delete(cls, project: Project or str):
        """
        Удалить объект
        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        project.delete()

    # TODO coming soon
    @classmethod
    def project_change_client(cls, project: Project or str, client: Client or str) -> Project:
        pass

    @classmethod
    def project_list(cls, **filters) -> list[Project]:
        """
        Возвращает список объектов всех доступных пользователю проектов. Если
        текущий пользователь имеет несколько проектов или ему предоставили
        доступ к стороннему проекту, данный список будет содержать их все.
        Args:
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов: class:`rcp.api.Project`
        """
        return Project().get_list(PROJECT_ENDPOINT, Project, **filters)

    @classmethod
    def project_vdc_list(cls, project: Project or str, **filters) -> list[Vdc]:
        """
        Получить ВЦОДы в данном проекте.
        Вернет список объектов :class:`rcp.api.Vdc`.

        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Vdc`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.get_list(VDC_ENDPOINT, Vdc, project=project.id, **filters)

    # TODO coming soon
    @classmethod
    def project_available_hypervisors_list(cls, project: Project or str, **filters) -> list[Hypervisor]:
        """
        Получить список доступных гипервизоров в этом проекте. Вернет список
        объектов :class:`rcp.api.Hypervisor`.

        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Hypervisor`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.get_list(HYPERVISOR_ENDPOINT, Hypervisor, project=project.id, **filters)

    @classmethod
    def project_dns_zones_list(cls, project: Project or str, **filters) -> list[Dns]:
        """
        Получить список доступных доменных зон в этом проекте.
        Вернет список объектов :class:`rcp.api.Dns`.

        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Dns`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.get_list(DNS_ENDPOINT, Dns, project=project.id, **filters)

    @classmethod
    def project_k8s_clusters_list(cls, project: Project or str, **filters) -> list[Kubernetes]:
        """
        Получить список доступных кластеров Kubernetes в этом проекте.
        Вернет список объектов :class:`rcp.api.Kubernetes`.

        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.Kubernetes`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.get_list(KUBERNETES_ENDPOINT, Kubernetes, project=project.id, **filters)

    @classmethod
    def project_s3_storages_list(cls, project: Project or str, **filters) -> list[S3]:
        """
        Получить список доступных s3 хранилищ в этом проекте. Вернет список
        объектов :class:`rcp.api.S3`.

        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.S3`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.get_list(S3_ENDPOINT, S3, project=project.id, **filters)

    @classmethod
    def project_paas_templates_list(cls, project: Project or str, **filters) -> list[PaasTemplate]:
        """
        Получить список доступных PaaS шаблонов в этом проекте. Вернет список
        объектов :class:`rcp.api.PaasTemplate`.

        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.PaasTemplate`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.get_list(PAAS_TEMPLATE_ENDPOINT, PaasTemplate, project_id=project.id, **filters)

    @classmethod
    def project_paas_services_list(cls, project: Project or str, **filters) -> list[PaasService]:
        """
        Получить список доступных PaaS сервисов в этом проекте. Вернет список
        объектов :class:`rcp.api.PaasService`.

        Args:
            project (object, str): Объект класса :class:`rcp.api.Project` или его id
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.PaasService`
        """
        if type(project) is str:
            project = Project().retrieve(id=project)
        return project.get_list(PAAS_SERVICE_ENDPOINT, PaasService, project_id=project.id, **filters)
