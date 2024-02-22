from esu.base import BaseAPI, Field


class Platform(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        hypervisor (object): Объект класса :class:`esu.Hypervisor`.
                             Гипервизор платформы

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
        hypervisor = Field('esu.Hypervisor')

    @classmethod
    def get_object(cls, id):
        """
        Получить объект проекта по его ID

        Args:
            id (str): Идентификатор проекта

        Returns:
            object: Возвращает объект проекта :class:`esu.Platform`
        """
        platform = cls(id=id)
        platform._get_object('v1/platform', platform.id)
        return platform
