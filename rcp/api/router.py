from .base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId, resolve
from rcp.api.consts import ROUTER_ENDPOINT, PORT_ENDPOINT


class Router(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        vdc (object): ВЦОД, к которому относится маршрутизатор :class:`rcp.api.Vdc`
        is_default (bool): True для маршрутизатора по умолчанию
        floating (object): Порт подключения к внешней сети :class:`rcp.api.Port`
        ports (list): Список подключений маршрутизатора

    .. note:: Поля ``name``, ``ports`` и ``vdc`` необходимы для создания.

              Поле ``floating`` опционально при создании.

              Поля ``name`` и ``floating`` могут быть изменены для
              существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('rcp.api.Vdc')
        is_default = Field()
        floating = Field('rcp.api.Port', allow_none=True)
        ports = FieldList('rcp.api.Port')

    @classmethod
    def retrieve(cls, id):
        """
        Получить объект маршрутизатора по его ID

        Args:
            id (str): Идентификатор маршрутизатора

        Returns:
            object: Возвращает объект маршрутизатора :class:`rcp.api.Router`
        """
        router = cls(id=id)
        router._get_object(ROUTER_ENDPOINT, router.id)
        return router

    def create(self, name, vdc, ports, wait, timeout, **kwargs):
        """
        Создать объект

        Raises:
            ObjectAlreadyHasId: Если производится попытка создать объект,
                                который уже существует
        """
        if self.id is not None:
            raise ObjectAlreadyHasId
        router = {
            'name': name,
            'vdc': vdc.id,
            'ports': [{'id': port.id} for port in ports]
        }
        for k, v in kwargs.items():
            router[k] = v
        # for k in self.__dict__:
        #     if k in locals():
        #         v = locals()[k]
        #         print(k)
        #         if isinstance(v, BaseAPI):
        #             router[k] = v.id
        #             print('1')
        #         elif (isinstance(v, str) or isinstance(v, int) or v is None or
        #               v is not isinstance(v, dict)):
        #             router[k] = v
        #             print('2')
        #         elif isinstance(v, dict):
        #             print('3')
        #             for k1 in v:
        #                 router[k1] = v[k1]
        self._commit_object(ROUTER_ENDPOINT, wait=wait, timeout=timeout, **router)
        return self

    # TODO coming soon
    def update(self, wait, timeout, **kwargs):
        """
        Сохранить изменения

        Raises:
            ObjectHasNoId: Если производится попытка сохранить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId
        router = {
            'name': self.name
        }
        floating = None
        if self.floating:
            # keep/change or get a new IP
            floating = self.floating.id or '0.0.0.0'

        print(router)
        # floating = None
        # if self.floating:
        #     # keep/change or get a new IP
        #     floating = self.floating.id or '0.0.0.0'

        for k, v in kwargs.items():
            router[k] = v
        return self._commit_object(ROUTER_ENDPOINT, wait=wait, timeout=timeout, **router)
        # self._commit()

    # def _commit(self):
    #     ports = [{
    #         'id': o.id
    #     } if o.id else {
    #         'network': o.network.id
    #     } for o in self.ports]
    #     floating = None
    #     if self.floating:
    #         # keep/change or get a new IP
    #         floating = self.floating.id or '0.0.0.0'
    #
    #     return self._commit_object('v1/router', vdc=self.vdc.id,
    #                                name=self.name, ports=ports,
    #                                floating=floating)

    def delete(self, wait, timeout):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object(ROUTER_ENDPOINT, self.id, wait=wait, timeout=timeout)
        self.id = None

    def add_port(self, port, wait, timeout):
        """
        Добавить подключение

        Args:
            port (object): Новый объект :class:`rcp.api.Port`
        """
        port = self._call('POST', PORT_ENDPOINT, router=self.id,
                          network=port.network.id, wait=wait, timeout=timeout)
        self.ports.append(resolve('rcp.api.Port')(token=self.token, **port))
        return self

    def remove_port(self, port, wait, timeout):
        """
        Удалить подключение

        Args:
            port (object): Существующий объект :class:`rcp.api.Port`
        """
        self._call('DELETE', '{}/{}'.format(PORT_ENDPOINT, port.id),
                   wait=wait, timeout=timeout)
        self.ports = [o for o in self.ports if o.id != port.id]
        return self
