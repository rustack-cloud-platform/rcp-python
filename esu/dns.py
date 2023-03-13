from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from esu.dns_record import DnsRecord


class Dns(BaseAPI):
    """
    Args:
        id (str): Идентификатор Dns
        name (str): Имя Dns
        project (object): Объект класса :class:`esu.Project`. Проект, к
                          которому относится данный Dns
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **ESU_API_TOKEN**

    .. note:: Поля ``name`` и ``project`` необходимы для
              создания.

              Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        project = Field('esu.Project')

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект Dns по его ID

        Args:
            id (str): Идентификатор Dns
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект Dns :class:`esu.Dns`
        """
        dns = cls(token=token, id=id)
        dns._get_object('v1/dns', dns.id)
        return dns

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
        self._commit_object('v1/dns', project=self.project.id, name=self.name)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/dns', self.id)
        self.id = None

    def get_dns_records(self):
        """
        Получить список днс записей, доступных в рамках данного Dns.

        Returns:
            list: Список объектов :class:`esu.DnsRecord`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/dns/{}/record'.format(self.id), DnsRecord)
