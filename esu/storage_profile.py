from esu.base import BaseAPI, Field


class StorageProfile(BaseAPI):
    """
    Args:
        id (str): Идентификатор профиля хранения
        name (str): Имя профиля хранения

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()

    @classmethod
    def get_object(cls, id):
        """
        Получить объект профиля хранения по его ID

        Args:
            id (str): Идентификатор профиля хранения

        Returns:
            object: Возвращает объект профиля хранения
            :class:`esu.StorageProfile`
        """
        storage_profile = cls(id=id)
        storage_profile._get_object('v1/storage_profile', storage_profile.id)
        return storage_profile
