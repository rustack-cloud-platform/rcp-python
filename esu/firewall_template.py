from esu.base import BaseAPI, Field


class FirewallTemplate(BaseAPI):
    """
    Args:
        id (str): Идентификатор шаблона брандмауэра
        name (str): Имя шаблона брандмауэра

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект шаблона брандмауэра по его ID

        Args:
            id (str): Идентификатор шаблона брандмауэра
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект шаблона брандмауэра
            :class:`esu.FirewallTemplate`
        """
        firewall = cls(token=token, id=id)
        firewall._get_object('v1/firewall', firewall.id)
        return firewall
