from .base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


# pylint: disable=invalid-name
class S3Bucket(BaseAPI):
    """
        Args:
            id (str): Идентификатор
            name (str): Имя бакета в ЕСУ
            external_name (str): Имя бакета в S3
    """
    class Meta:
        id = Field()
        name = Field()
        external_name = Field()

    @classmethod
    def get_object(cls, id, s3):
        """
        Получить объект бакета хранилища S3 по его ID

        Args:
            id (str): Идентификатор бакета хранилища S3
            s3: class:'rcp.S3'

        Returns:
            object: Возвращает объект бакета хранилища S3 :class:`rcp.S3bucket`
        """
        s3bucket = cls(id=id)
        s3bucket._get_object('v1/s3_storage/{}/bucket'.format(s3.id),
                             s3bucket.id)

        return s3bucket

    def create(self, s3):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit(s3)

    def save(self, s3):
        """
        Сохранить изменения
        """
        if self.id is None:
            raise ObjectHasNoId

        self._commit(s3)
        return self

    def _commit(self, s3):
        s3bucket = {'name': self.name}

        self._commit_object('v1/s3_storage/{}/bucket'.format(s3.id),
                            **s3bucket)

    def destroy(self, s3):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/s3_storage/{}/bucket'.format(s3.id), self.id)
        self.id = None
