from rcp.api.template import Template
from rcp.api.template_field import TemplateField


class TemplateMixin:

    @classmethod
    def template_retrieve(cls, id) -> Template:
        """
        Получить объект шаблона по его ID

        Args:
            id (str): Идентификатор шаблона

        Returns:
            object: Возвращает объект шаблона :class:`rcp.api.Template`
        """
        return Template().retrieve(id)

    @classmethod
    def template_field_retrieve(cls, template) -> list[TemplateField]:
        """
        Получить список полей шаблона ОС.

        Returns:
            list: Список объектов :class:`rcp.api.TemplateField`
        """
        if type(template) is str:
            template = Template().retrieve(id=template)
        return template.retrieve_fields()
