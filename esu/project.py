from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from esu.vdc import Vdc


class Project(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        client (object): Объект класса :class:`esu.Client`. Клиент, к которому
                         относится проект
        token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

    .. note:: Поля ``name`` и ``client`` необходимы для создания.

            Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        client = Field('esu.Client')

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект проекта по его ID

        Args:
            id (str): Идентификатор проекта
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект проекта :class:`esu.Project`
        """
        project = cls(token=token, id=id)
        project._get_object('v1/project', project.id)
        return project

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
        self._commit_object('v1/project', client=self.client.id,
                            name=self.name)

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
        :class:`esu.Vdc`.

        Returns:
            list: Список объектов :class:`esu.Vdc`
        """

        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/vdc', Vdc, project=self.id)

    def get_available_hypervisors(self):
        """
        Получить список доступных гипервизоров в этом проекте. Вернет список
        объектов :class:`esu.Hypervisor`.

        Returns:
            list: Список объектов :class:`esu.Hypervisor`
        """

        return self.client.allowed_hypervisors
