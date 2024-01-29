from .base import BaseAPI, Field, ObjectAlreadyHasId, \
    ObjectHasNoId
from .consts import PROJECT_ENDPOINT
from .client import Client


class Project(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        client (object): Объект класса :class:`rcp.api.Client`. Клиент, к которому
                         относится проект

    .. note:: Поля ``name`` и ``client`` необходимы для создания.

            Поле ``name`` может быть изменено для существующего объекта.
    """

    class Meta:
        id = Field()
        name = Field()
        client = Field('rcp.api.Client')
        tags = Field()

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект проекта по его ID

        Args:
            id (str): Идентификатор проекта

        Returns:
            object: Возвращает объект проекта :class:`rcp.api.Project`
        """
        project = cls(id=id)
        project._get_object(PROJECT_ENDPOINT, project.id)
        return project

    def create(self, name: str, client: Client or str, **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit_object(PROJECT_ENDPOINT, name=name, client=client, **kwargs)
        return self

    def update(self, **kwargs):
        """
        Сохранить изменения

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId
        project = {
            'name': self.name,
            'tags': [tag.get('name') for tag in self.tags]
        }
        for k, v in kwargs.items():
            project[k] = v
        self._commit_object(PROJECT_ENDPOINT, **project)
        return self

    def delete(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(PROJECT_ENDPOINT, self.id)
        self.id = None

    # TODO coming soon
    def change_client(self, client: Client or str):
        pass

    # TODO will move to ..
    # def get_available_hypervisors(self):
        # """
        # Получить список доступных гипервизоров в этом проекте. Вернет список
        # объектов :class:`rcp.Hypervisor`.
        #
        # Returns:
        #     list: Список объектов :class:`rcp.api.Hypervisor`
        # """
        #
        # return self.client.allowed_hypervisors


