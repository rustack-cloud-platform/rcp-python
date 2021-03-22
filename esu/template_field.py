from esu.base import BaseAPI, Field


class TemplateField(BaseAPI):
    """
    Args:
        id (str): Идентификатор поля шаблона
        name (str): Имя поля шаблона
        default (str): Значение по умолчанию
        type (str): Тип
        required (boolean): Обязательное
        position (int): Порядок
        system_alias (str): Системный идентификатор

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
        default = Field()
        type = Field()
        required = Field()
        position = Field()
        system_alias = Field()
