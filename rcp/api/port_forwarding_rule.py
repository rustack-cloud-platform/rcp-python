from .base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class PortForwardingRule(BaseAPI):
    """
    Args:
        id (str): Идентификатор правила перенаправления портов
        port (object): Объект класса :class:`rcp.Port`. Порт сервера до
                       которого осуществляется перенаправление
        internal_port (int): Внутренний порт устройства, с которого
                             осуществляется перенаправление
        external_port (int): Внешний порт устройства, на который
                             осуществляется перенаправление
        protocol (str): Протокол по которому будет осуществляться
                        перенаправление

    .. note:: Управление перенаправлением портов создаваемом на порте возможно
              только в ресурсном пуле под управлением Openstack.
              Поля ``external_port``, ``internal_port``, ``protocol``
              необходимы для создания.

    """
    class Meta:
        port_forwarding = Field('rcp.PortForwarding')
        port = Field('rcp.Port')
        id = Field()
        external_port = Field()
        internal_port = Field()
        protocol = Field()

    @classmethod
    def get_object(cls, port_forwarding, rule_id):
        """
        Получить объект маршрута на роутере по его ID

        Args:
            rule_id (str): Идентификатор маршрута на роутере

        Returns:
            object: Возвращает объект маршрута на роутере
            :class:`rcp.RouterRoute`
        """
        pf_rule = cls(id=rule_id, port_forwarding=port_forwarding)
        pf_rule._get_object(
            'v1/port_forwarding/'
            '{}/rule'.format(pf_rule.port_forwarding.id), pf_rule.id)
        return pf_rule

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
        port_forwarding_rule = {
            "internal_port": self.internal_port,
            "external_port": self.external_port,
            "protocol": self.protocol,
            "port": self.port.id
        }

        self._commit_object(
            'v1/port_forwarding/'
            '{}/rule'.format(self.port_forwarding.id), **port_forwarding_rule)

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
            'v1/port_forwarding/'
            '{}/rule'.format(self.port_forwarding.id), self.id)
        self.id = None
