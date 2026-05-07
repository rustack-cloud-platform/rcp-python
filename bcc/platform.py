from bcc.base import BaseAPI, Field


class Platform(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        hypervisor (object): Объект класса :class:`bcc.Hypervisor`.
                             Гипервизор платформы
        token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **BCC_API_TOKEN**

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
        hypervisor = Field('bcc.Hypervisor')

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект проекта по его ID

        Args:
            id (str): Идентификатор проекта
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **BCC_API_TOKEN**

        Returns:
            object: Возвращает объект проекта :class:`bcc.Platform`
        """
        platform = cls(token=token, id=id)
        platform._get_object('v1/platform', platform.id)
        return platform
