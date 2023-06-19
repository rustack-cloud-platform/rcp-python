from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class RouterRoute(BaseAPI):
    """
    Args:
        id (str): Идентификатор маршрута
        router (object): Объект класса :class:`esu.Router`. Роутер, к
                         которому относится данное правило
        destination (str): CIDR сети в которую будет маршрутизирован трафик
        nexthop (str): Адрес шлюза - роутера в сети из которой будет
                       осуществляться маршрутизация, подключенного к исходной
                       сети и к сети в которую будет маршрутизироваться трафик
        token (str): Токен для доступа к API. Если не передан, будет
            использована переменная окружения **ESU_API_TOKEN**

    .. note:: Поля ``destination``, ``nexthop``, необходимы для создания.

    """
    class Meta:
        id = Field()
        router = Field('esu.Router')
        nexthop = Field()
        destination = Field()

    @classmethod
    def get_object(cls, router, route_id, token=None):
        """
        Получить объект маршрута на роутере по его ID

        Args:
            id (str): Идентификатор маршрута на роутере
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект маршрута на роутере
            :class:`esu.RouterRoute`
        """
        route = cls(token=token, id=route_id, router=router)
        route._get_object('v1/router/{}/route'.format(route.router.id),
                          route.id)
        return route

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
        route = {"nexthop": self.nexthop, "destination": self.destination}

        self._commit_object('v1/router/{}/route'.format(self.router.id),
                            **route)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/router/{}/route'.format(self.router.id),
                             self.id)
        self.id = None
