from esu.base import BaseAPI, Field


class VmMetadata(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        field (object): Объект :class:`esu.TemplateField`
        value (str): Значение
    """
    class Meta:
        id = Field()
        field = Field('esu.TemplateField')
        value = Field()
