from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class RouterFirewallRule(BaseAPI):
    """
    Args:
        id (str): Идентификатор правила брандмауэра
        name (str): Имя правила брандмауэра
        router (object): Объект класса :class:`esu.Router`. Роутер, к
                         которому относится данное правило брандмауэра
        direction (str): Направление правила брандмауэра
        source_ip (str): Адрес источника правила брандмауэра (может быть IP
                         адресом или CIDR, None = любой)
        src_port_range_max (str): Максимальный порт диапазона портов источника
        src_port_range_min (str): Минимальный порт диапазона портов источника

        destination_ip (str): Адрес назначения правила брандмауэра (может
                              быть IP адресом или CIDR, None = любой)
        dst_port_range_max (str): Максимальный порт диапазона портов назначения
        dst_port_range_min (str): Минимальный порт диапазона портов назначения
        protocol (str): protocol правила брандмауэра

    .. note:: Управление брандмауэром на роутере доступно только для ресурсного
              пула VMware.
              Поля ``direction``, ``name`` и ``protocol`` необходимы
              для создания.

    """
    class Meta:
        router = Field('esu.Router')
        id = Field()
        name = Field()
        direction = Field()
        source_ip = Field(allow_none=True)
        src_port_range_max = Field(allow_none=True)
        src_port_range_min = Field(allow_none=True)
        destination_ip = Field(allow_none=True)
        dst_port_range_max = Field(allow_none=True)
        dst_port_range_min = Field(allow_none=True)
        protocol = Field()

    @classmethod
    def get_object(cls, router, rule_id):
        """
        Получить объект правила брандмауэра роутера по его ID

        Args:
            rule_id (str): Идентификатор правила брандмауэра на роутере
            router: class:'esu.Router'

        Returns:
            object: Возвращает объект правила брандмауэра на роутере
            :class:`esu.RouterFirewallRule`
        """
        firewall_rule = cls(id=rule_id, router=router)
        firewall_rule._get_object(
            'v1/router/{}/firewall_rule'.format(firewall_rule.router.id),
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
        router_fw_rule = {
            "name": self.name,
            "destination_ip": self.destination_ip,
            "source_ip": self.source_ip,
            "src_port_range_max": self.src_port_range_max,
            "src_port_range_min": self.src_port_range_min,
            "direction": self.direction,
            "dst_port_range_max": self.dst_port_range_max,
            "dst_port_range_min": self.dst_port_range_min,
            "protocol": self.protocol
        }
        self._commit_object(
            'v1/router/{}/'
            'firewall_rule'.format(self.router.id), **router_fw_rule)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(
            'v1/router/{}/firewall_'
            'rule'.format(self.router.id), self.id)
        self.id = None
