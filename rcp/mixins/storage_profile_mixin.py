from rcp.api.consts import STORAGE_PROFILE_ENDPOINT
from rcp.api.storage_profile import StorageProfile
from rcp.api.base import BaseAPI


class StorageProfileMixin:

    @classmethod
    def storage_profile_retrieve(cls, id: str) -> StorageProfile:
        """
        Получить объект профиля хранения по его ID

        Args:
            id (str): Идентификатор профиля хранения

        Returns:
            object: Возвращает объект профиля хранения
            :class:`rcp.api.StorageProfile`
        """
        return StorageProfile().retrieve(id)

    @classmethod
    def storage_profile_list(cls, **filters) -> list[StorageProfile]:
        """
        Получить список профилей хранения, которые используются при добавлении
        дисков.

        Args:
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            list: Список объектов :class:`rcp.api.StorageProfile`
        """
        return StorageProfile().get_list(STORAGE_PROFILE_ENDPOINT, StorageProfile, **filters)
