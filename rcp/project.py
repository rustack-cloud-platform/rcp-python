from rcp.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from rcp.dns import Dns
from rcp.kubernetes import Kubernetes
from rcp.s3 import S3
from rcp.vdc import Vdc
from rcp.client import Client


class Project(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        client (object): Объект класса :class:`rcp.Client`. Клиент, к которому
                         относится проект

    .. note:: Поля ``name`` и ``client`` необходимы для создания.

            Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        client = Field('rcp.Client')

    @classmethod
    def get_object(cls, id):
        """
        Получить объект проекта по его ID

        Args:
            id (str): Идентификатор проекта

        Returns:
            object: Возвращает объект проекта :class:`rcp.Project`
        """
        project = cls(id=id)
        project._get_object('v1/project', project.id)
        return project

    def create(self, name: str, client: Client, **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit_object('v1/project', name=name,
                            client=client, **kwargs)
        return self

    def update(self, **kwargs):
        """
        Сохранить изменения

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        # if self.id is None:
        #     raise ObjectHasNoId
        project = {}
        # for key in self._rules:
        #     if isinstance(getattr(self, key), :
        #         project[key] = getattr(self, key).id
        #         print(type(getattr(self, key)))
        #     else:
        #         project[key] = getattr(self, key)
        # print(project)

        for key, value in kwargs.items():
            project[key] = value
            # elif key not in kwargs:
            #     project[key] = value
            # value = getattr(self, key)
            # print(key, '====', value)
            # project[key] = value
        # for key, value in kwargs.items():
        #     project[key] = value

        # for key, value in kwargs.items():
        #     if key not in self._rules:
        #         project[key] = value
        #     else:
        #         project[key] = value
        # name = name or self.name
        print(project)
        self._commit_object('v1/project', **project)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/project', self.id)
        self.id = None

    def get_vdcs(self):
        """
        Получить ВЦОДы в данном проекте. Вернет список объектов
        :class:`rcp.Vdc`.

        Returns:
            list: Список объектов :class:`rcp.Vdc`
        """

        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/vdc', Vdc, project=self.id)

    def get_available_hypervisors(self):
        """
        Получить список доступных гипервизоров в этом проекте. Вернет список
        объектов :class:`rcp.Hypervisor`.

        Returns:
            list: Список объектов :class:`rcp.Hypervisor`
        """

        return self.client.allowed_hypervisors

    def get_dns_zones(self):
        """
        Получить список доступных доменных зон в этом проекте. Вернет список
        объектов :class:`rcp.Dns`.

        Returns:
            list: Список объектов :class:`rcp.Dns`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/dns', Dns, project=self.id)

    def get_k8s_clusters(self):
        """
        Получить список доступных кластеров Kubernetes в этом проекте.
        Вернет список объектов :class:`rcp.Kubernetes`.

        Returns:
            list: Список объектов :class:`rcp.Kubernetes`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/kubernetes', Kubernetes, project=self.id)

    def get_s3_storages(self):
        """
        Получить список доступных s3 хранилищ в этом проекте. Вернет список
        объектов :class:`rcp.S3`.

        Returns:
            list: Список объектов :class:`rcp.S3`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/s3_storage', S3, project=self.id)

    def get_paas_templates(self):
        """
        Получить список доступных PaaS шаблонов в этом проекте. Вернет список
        объектов :class:`rcp.PaasTemplate`.

        Returns:
            list: Список объектов :class:`rcp.PaasTemplate`
        """
        if self.id is None:
            raise ObjectHasNoId
        return self._get_list('v1/paas_template', 'rcp.PaasTemplate',
                              project_id=self.id)
