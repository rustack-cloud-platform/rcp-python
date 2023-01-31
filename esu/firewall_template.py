from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from esu.firewall_template_rule import FirewallTemplateRule


class FirewallTemplate(BaseAPI):
    """
    Args:
        id (str): Идентификатор шаблона брандмауэра
        name (str): Имя шаблона брандмауэра
        vdc (object): Объект класса :class:`esu.Vdc`. ВЦОД, к которому
                      относится данный шаблон файрвола
        description (str): описание для шаблона брандмауэра

    .. warning:: Объект доступен только для чтения и не может быть создан,
                 изменен или удален.
    """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('esu.Vdc')
        description = Field()

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

    def save(self):
        """
        Сохранить изменения

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._commit()

    def _commit(self):
        self._commit_object('v1/firewall', vdc=self.vdc.id, name=self.name,
                            description=self.description)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/firewall', self.id)
        self.id = None

    def get_firewall_rules(self):
        """
        Получить список правил файрвола,
        доступных в рамках данного шаблона брандмауэра.

        Returns:
            list: Список объектов :class:`esu.FirewallTemplateRule`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list('v1/firewall/{}/rule'.format(self.id),
                              FirewallTemplateRule)
