from rcp.api.consts import CLIENT_ENDPOINT
from rcp.api.client import Client


class ClientMixin:

    @classmethod
    def client_retrieve(cls, id: str) -> Client:
        """
        Получить объект клиента по его ID

        Args:
            id (str): Идентификатор клиента
            filters (**kwargs): Список параметров для фильтрации списка ключ=значение

        Returns:
            object: Возвращает объект клиента :class:`rcp.api.Client`

        .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
        """
        return Client().retrieve(id)

    @classmethod
    def client_balance(cls, client: Client or str) -> float:
        """
        Получить баланс клиента

        Args:
            client (object, str): Объект класса :class:`rcp.api.Client` или его id.

        Returns:
            float: Возвращает float
        """
        if type(client) is str:
            client = Client().retrieve(id=client)
        return client.balance

    # TODO coming soon
    # @classmethod
    # def clients_list(cls, client: Client or str, **filters):
    #     """
    #     Возвращает список объектов всех доступных пользователю клиентов. Если
    #     текущему пользователю был предоставлен доступ к еще одному клиенту,
    #     данный список будет содержать два элемента.
    #
    #     Returns:
    #         list: Список объектов: class:`rcp.api.Client`
    #     """
    #     return self._get_list('v1/client', 'rcp.Client')
