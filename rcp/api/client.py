from .base import BaseAPI, Field, FieldList
from rcp.api.consts import CLIENT_ENDPOINT


class Client(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        payment_model (str): Модель взаиморасчетов. **prepay** или **postpay**
        balance (float): Баланс

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
        allowed_hypervisors = FieldList('rcp.api.Hypervisor')
        payment_model = Field()
        billing_enabled = Field()

    @property
    def balance(self):
        return self.kwargs['contract']['balance']

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект клиента по его ID

        Args:
            id (str): Идентификатор клиента

        Returns:
            object: Возвращает объект клиента :class:`rcp.api.Client`
        """
        client = cls(id=id)
        client._get_object(CLIENT_ENDPOINT, client.id)
        return client
