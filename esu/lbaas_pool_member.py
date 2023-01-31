from esu.base import BaseAPI, Field


class LbaasPoolMember(BaseAPI):
    """
    Args:
        port (str): Идентификатор
        vm (object): Объект :class:`esu.TemplateField`
        weight (str): Значение
    """
    class Meta:
        port = Field()
        vm = Field('esu.Vm')
        weight = Field()
