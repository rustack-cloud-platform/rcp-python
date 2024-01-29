from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class FirewallTemplateRule(BaseAPI):
    """
    Args:
        id (str): Идентификатор правила брандмауэра
        name (str): Имя правила брандмауэра
        firewall (str): Объект класса :class:`esu.FirewallTemplate`.
                Шаблон брандмауэра, к которому относится данное правило
                брандмауэра
        direction (str): направление правила брандмауэра
        destination_ip (str): destination_ip правила брандмауэра
        dst_port_range_max (str): dst_port_range_max правила брандмауэра
        dst_port_range_min (str): dst_port_range_min правила брандмауэра
        protocol (str): protocol правила брандмауэра

    .. note:: Поля ``direction``, ``name`` и ``protocol`` необходимы для
              создания.

    """
    class Meta:
        id = Field()
        name = Field()
        firewall = Field('esu.FirewallTemplate')
        direction = Field()
        destination_ip = Field()
        dst_port_range_max = Field()
        dst_port_range_min = Field()
        protocol = Field()

    @classmethod
    def get_object(cls, firewall, rule_id):
        """
        Получить объект правил брандмауэра по его ID

        Args:
            id (str): Идентификатор правила шаблона брандмауэра

        Returns:
            object: Возвращает объект правила шаблона брандмауэра
            :class:`esu.FirewallTemplateRule`
        """
        firewall_rule = cls(id=rule_id, firewall=firewall)
        firewall_rule._get_object(
            'v1/firewall/{}/rule'.format(firewall_rule.firewall.id),
            firewall_rule.id)
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
            'v1/firewall/{}/rule'.format(self.firewall.id),
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

        self._destroy_object('v1/firewall/{}/rule'.format(self.firewall.id),
                             self.id)
        self.id = None
