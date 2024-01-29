from esu.base import BaseAPI, Field


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
    def get_object(cls, id):
        """
        Получить объект шаблона по его ID

        Args:
            id (str): Идентификатор шаблона

        Returns:
            object: Возвращает объект шаблона :class:`esu.Template`
        """
        template = cls(id=id)
        template._get_object('v1/template', template.id)
        return template

    def get_fields(self):
        """
        Получить список полей шаблона ОС.

        Returns:
            list: Список объектов :class:`esu.TemplateField`
        """
        return self._get_list('v1/template/{}/field'.format(self.id),
                              'esu.TemplateField', False)
