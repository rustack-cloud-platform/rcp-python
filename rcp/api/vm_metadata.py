from .base import BaseAPI, Field


class VmMetadata(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        field (object): Объект :class:`rcp.TemplateField`
        value (str): Значение
    """
    class Meta:
        id = Field()
        field = Field('rcp.TemplateField')
        value = Field()
