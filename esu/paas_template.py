from esu.base import BaseAPI, Field


class PaasTemplate(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        description (str): Описание
    """
    class Meta:
        id = Field()
        name = Field()
        description = Field()

    @classmethod
    def get_object(cls, id, project_id):
        """
        Получить объект шаблона по его ID

        Args:
            id (str): Идентификатор шаблона
            project_id (str): Идентификатор проекта

        Returns:
            object: Возвращает объект шаблона :class:`esu.PaasTemplate`
        """
        template = cls(id=id)
        template._get_object('v1/paas_template', template.id, project_id)
        return template

    def _get_object(self, resource, id, project_id):
        self.kwargs = self._call('GET', '{}/{}'.format(resource, id),
                                 project_id=project_id)
        self._fill()

    def get_inputs(self, project_id):
        """
        Получить описания полей

        Returns:
            dict: Описания полей {"inputs": [...]}
        """
        data = self._call('GET', 'v1/paas_template/{}/inputs'.format(self.id),
                          project_id=project_id)
        return data
