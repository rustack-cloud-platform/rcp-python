from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


# pylint: disable=invalid-name
class S3(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        project (object): Объект класса :class:`esu.Project`. Проект,
                        к которому относится данное хранилище
        access_key (str): Ключ доступа к хранилищу
        secret_key (str): Секретный ключ доступа к хранилищу
        client_endpoint (str): URL для подключения к хранилищу
    """
    class Meta:
        id = Field()
        name = Field()
        project = Field('esu.Project')
        backend = Field()
        access_key = Field()
        secret_key = Field()
        client_endpoint = Field()

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект хранилища S3 по его ID

        Args:
            id (str): Идентификатор хранилища S3
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект хранилища S3 :class:`esu.S3`
        """
        s3 = cls(token=token, id=id)
        s3._get_object('v1/s3_storage', s3.id)

        return s3

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
        s3 = {'project': self.project.id, 'name': self.name}
        if self.backend is not None:
            s3['backend'] = self.backend
        self._commit_object('v1/s3_storage', **s3)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/s3_storage', self.id)
        self.id = None

    def renew_keys(self):
        """
        Сгенерировать новые ключи
        """
        self._call('POST', 'v1/s3_storage/{}/renew'.format(self.id))
        obj = self.get_object(id=self.id)
        self.kwargs = obj.kwargs
        self._fill()
        return self
