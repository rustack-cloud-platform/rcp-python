from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class PaasService(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        project (object): Объект :class:`esu.Project`
        paas_service_id (int): Идентификатор шаблона
        paas_deploy_id (int): Идентификатор развёртывания
        status (str): Статус
        inputs (dict): Входные параметры
        """
    class Meta:
        id = Field()
        name = Field()
        project = Field('esu.Project')
        paas_service_id = Field()
        paas_deploy_id = Field()
        status = Field()
        paas_service_inputs = Field()

    @classmethod
    def get_object(cls, id):
        """
        Получить объект PaasService по его ID

        Args:
            id (str): Идентификатор

        Returns:
            object: Возвращает объект кластера
            paas_service :class:`esu.PaasService`
        """
        service = cls(id=id)
        service._get_object('v1/paas_service', service.id)

        return service

    def create(self):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
            который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId

        self._commit()

    def _commit(self):
        service = {
            'name': self.name,
            'project': self.project.id,
            'paas_service_id': self.paas_service_id,
            'paas_service_inputs': self.paas_service_inputs,
        }
        self._commit_object('v1/paas_service', **service)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/paas_service', self.id)
        self.id = None
