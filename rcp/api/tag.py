from .base import BaseAPI, Field


class Tag(BaseAPI):
    """
    Args:
        id (str): Идентификатор тэга
        name (str): Имя тэга
    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
