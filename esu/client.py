from esu.base import BaseAPI, Field, FieldList


class Client(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        payment_model (str): Модель взаиморасчетов. **prepay** или **postpay**
        balance (float): Баланс
        token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
        allowed_hypervisors = FieldList('esu.Hypervisor')
        payment_model = Field()
        billing_enabled = Field()

    @property
    def balance(self):
        return self.kwargs['contract']['balance']

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект клиента по его ID

        Args:
            id (str): Идентификатор клиента
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект клиента :class:`esu.Client`
        """
        client = cls(token=token, id=id)
        client._get_object('v1/client', client.id)
        return client

    def get_projects(self):
        """
        Получить проекты данного клиента.

        Returns:
            list: Список объектов :class:`esu.Project`
        """
        return self._get_list('v1/project', 'esu.Project', client=self.id)
