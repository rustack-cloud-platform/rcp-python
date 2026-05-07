from bcc.base import BaseAPI, Field, FieldList


class Client(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        payment_model (str): Модель взаиморасчетов. **prepay** или **postpay**
        balance (float): Баланс
        token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **BCC_API_TOKEN**

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
        allowed_hypervisors = FieldList('bcc.Hypervisor')
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
                         использована переменная окружения **BCC_API_TOKEN**

        Returns:
            object: Возвращает объект клиента :class:`bcc.Client`
        """
        client = cls(token=token, id=id)
        client._get_object('v1/client', client.id)
        return client

    def get_projects(self):
        """
        Получить проекты данного клиента.

        Returns:
            list: Список объектов :class:`bcc.Project`
        """
        return self._get_list('v1/project', 'bcc.Project', client=self.id)
