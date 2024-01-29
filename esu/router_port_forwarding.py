from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class RouterPortForwarding(BaseAPI):
    """
    Args:
        id (str): Идентификатор правила перенаправления портов
        router (object): Объект класса :class:`esu.Router`. Роутер, к
                         которому относится данное правило
        protocol (str): Протокол для которого осуществляется перенаправление
        local_ip (str): IP адрес сервера для которого создаётся правило
                    перенаправления портов.
        external_port_range_start (int): Старт диапазона портов сервера, для
                                    которого осуществляется перенаправление
        external_port_range_end (int): Конец диапазона портов сервера для
                                    которого осуществляется перенаправление
        internal_port (int): Порт роутера, по которому доступен сервер
                            для которого, создаётся правило перенаправления

    .. note:: Управление перенаправлением портов на роутере доступно только
              для ресурсного пула VMware.

              Поля ``protocol``, ``external_port_range_start``,
              ``external_port_range_end``, ``local_ip`` необходимы
              для создания.

    """
    class Meta:
        router = Field('esu.Router')
        id = Field()
        external_port_range_end = Field()
        external_port_range_start = Field()
        internal_port = Field()
        local_ip = Field()
        protocol = Field()

    @classmethod
    def get_object(cls, router, pf_id):
        """
        Получить объект правила перенаправления портов роутера по его ID

        Args:
            pf_id (str): Идентификатор правила перенаправления портов роутера
            router: class:'esu.Router'

        Returns:
            object: Возвращает объект правила перенаправления портов на роутере
            :class:`esu.RouterPortForwarding`
        """
        port_forwarding = cls(id=pf_id, router=router)
        port_forwarding._get_object(
            'v1/router/{}/port_forwarding'.format(port_forwarding.router.id),
            port_forwarding.id)
        return port_forwarding

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
        port_forwarding = {
            "internal_port": self.internal_port,
            "external_port_range_end": self.external_port_range_end,
            "external_port_range_start": self.external_port_range_start,
            "local_ip": self.local_ip,
            "protocol": self.protocol
        }

        self._commit_object(
            'v1/router/{}/'
            'port_forwarding'.format(self.router.id), **port_forwarding)

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
            'v1/router/{}/port_forwarding'.format(self.router.id), self.id)
        self.id = None
