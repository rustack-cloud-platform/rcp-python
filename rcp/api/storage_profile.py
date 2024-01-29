from .base import BaseAPI, Field
from rcp.api.consts import STORAGE_PROFILE_ENDPOINT


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
    def retrieve(cls, id):
        """
        Получить объект профиля хранения по его ID

        Args:
            id (str): Идентификатор профиля хранения

        Returns:
            object: Возвращает объект профиля хранения
            :class:`rcp.api.StorageProfile`
        """
        storage_profile = cls(id=id)
        storage_profile._get_object(STORAGE_PROFILE_ENDPOINT, storage_profile.id)
        return storage_profile
