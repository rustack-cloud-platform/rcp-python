from .base import BaseAPI, Field
from rcp.api.consts import TEMPLATE_ENDPOINT


class Template(BaseAPI):
    """
    Args:
        id (str): Идентификатор шаблона
        name (str): Имя шаблона
        min_cpu (int): Минимальное количество ядер, необходимое для
                       развертывания этого шаблона
        min_ram (int): Минимальное количество RAM, необходимое для
                       развертывания этого шаблона
        min_hdd (int): Минимальный размер первого диска, необходимого для
                       развертывания этого шаблона

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """

    class Meta:
        id = Field()
        name = Field()
        min_cpu = Field()
        min_ram = Field()
        min_hdd = Field()

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект шаблона по его ID

        Args:
            id (str): Идентификатор шаблона

        Returns:
            object: Возвращает объект шаблона :class:`rcp.api.Template`
        """
        template = cls(id=id)
        template._get_object(TEMPLATE_ENDPOINT, template.id)
        return template

    def retrieve_fields(self):
        """
        Получить список полей шаблона ОС.

        Returns:
            list: Список объектов :class:`rcp.api.TemplateField`
        """
        return self.get_list('{}/{}/field'.format(TEMPLATE_ENDPOINT, self.id),
                             'rcp.api.TemplateField', False)
