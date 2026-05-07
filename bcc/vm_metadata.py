from bcc.base import BaseAPI, Field


class VmMetadata(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        field (object): Объект :class:`bcc.TemplateField`
        value (str): Значение
    """
    class Meta:
        id = Field()
        field = Field('bcc.TemplateField')
        value = Field()
