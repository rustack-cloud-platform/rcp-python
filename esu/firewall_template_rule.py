from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class FirewallTemplateRule(BaseAPI):
    """
    Args:
        id (str): Идентификатор шаблона брандмауэра
        name (str): Имя шаблона брандмауэра
        firewall_id (str): Объект класса :class:`esu.FirewallTemplate`.
                Проект, к которому относится данное правило брандмауэра
        direction (str): direction шаблона брандмауэра
        destination_ip (str): destination_ip шаблона брандмауэра
        dst_port_range_max (str): dst_port_range_max шаблона брандмауэра
        dst_port_range_min (str): dst_port_range_min шаблона брандмауэра
        protocol (str): protocol шаблона брандмауэра
        token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

    .. note:: Поля ``direction``, ``name`` и ``protocol`` необходимы для
              создания.

    """
    class Meta:
        id = Field()
        name = Field()
        firewall_id = Field('esu.FirewallTemplate')
        direction = Field()
        destination_ip = Field()
        dst_port_range_max = Field()
        dst_port_range_min = Field()
        protocol = Field()

    @classmethod
    def get_object(cls, firewall_id, rule_id, token=None):
        """
        Получить объект правил брандмауэра по его ID

        Args:
            id (str): Идентификатор шаблона брандмауэра
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект шаблона брандмауэра
            :class:`esu.FirewallTemplateRule`
        """
        firewall_rule = cls(token=token, id=rule_id, firewall_id=firewall_id)
        firewall_rule._get_object(
            f'v1/firewall/{firewall_rule.firewall_id}/rule', firewall_rule.id)
        return firewall_rule

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
        self._commit_object(
            f'v1/firewall/{self.firewall_id}/rule',
            name=self.name,
            destination_ip=self.destination_ip,
            direction=self.direction,
            dst_port_range_max=self.dst_port_range_max,
            dst_port_range_min=self.dst_port_range_min,
            protocol=self.protocol,
        )

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(f'v1/firewall/{self.firewall_id}/rule', self.id)
        self.id = None
