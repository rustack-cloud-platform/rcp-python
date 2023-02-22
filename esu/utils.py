from esu.base import BaseAPI, Field


class LbaasPoolMember(BaseAPI):
    """
    Args:
        port (str): Порт участника пула балансировщика
        vm (object): Объект :class:`esu.Vm`
        weight (str): Вес участника пула балансировщика
    """
    class Meta:
        port = Field()
        vm = Field('esu.Vm')
        weight = Field()


class ConnectedObject(BaseAPI):
    """
    Args:
        id (str): Идентификатор подключённого объекта
        type (object): Тип объекта
        name (object): Имя подключённого объекта
        vdc (str): Объект :class:`esu.Vdc`
    """
    class Meta:
        id = Field()
        type = Field()
        name = Field()
        vdc = Field('esu.Vdc')
