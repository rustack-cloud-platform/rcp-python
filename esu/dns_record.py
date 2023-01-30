from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class DnsRecord(BaseAPI):
    """
    Args:
        id (str): Идентификатор Dns записи
        dns_id (str): Объект класса :class:`esu.Dns`. Днс зона, к
                          которому относится днс запись
        data (str): дата Dns записи
        flag (str): флаг Dns записи
        host (str): хост Dns записи
        port (str): порт Dns записи
        priority (str): приоритет Dns записи
        tag (str): тэг Dns записи
        ttl (str): ttl Dns записи
        type (str): тип Dns записи
        weight (str): вес Dns записи
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **ESU_API_TOKEN**

    .. note:: Поля ``data``, ``dns``, ``host``,
                    ``ttl``, ``type`` необходимы для создания.

    """
    class Meta:
        id = Field()
        dns_id = Field('esu.Dns')
        data = Field()
        flag = Field()
        host = Field()
        port = Field()
        priority = Field()
        tag = Field()
        ttl = Field()
        type = Field()
        weight = Field()

    @classmethod
    def get_object(cls, dns_id, id, token=None):
        """
        Получить объект Dns запись по его ID

        Args:
            id (str): Идентификатор Dns записи
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект Dns :class:`esu.DnsRecord`
        """
        dns_record = cls(token=token, id=id, dns_id=dns_id)
        dns_record._get_object(f'v1/dns/{dns_record.dns_id}/record',
                               dns_record.id)
        return dns_record

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
        self._commit_object(f'v1/dns/{self.dns_id}/record', data=self.data,
                            flag=self.flag, host=self.host, port=self.port,
                            priority=self.priority, tag=self.tag, ttl=self.ttl,
                            weight=self.weight)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(f'v1/dns/{self.dns_id}/record', self.id)
        self.id = None
