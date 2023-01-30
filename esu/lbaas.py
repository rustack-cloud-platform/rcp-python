from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId
from esu.lbaas_pool import LbaasPool


class Lbaas(BaseAPI):
    """
    Args:
        id (str): Идентификатор Lbaas
        name (str): Имя Lbaas
        vdc (object): Объект класса :class:`esu.Vdc`. ВЦОД, к которому
                      относится данный балансировщик нагрузки
        floating (object): Объект класса :class:`esu.Port`. Порт подключения
                           виртаульаного выделенного сервера к внешней сети.
                           Если None, сервер не имеет подключения к внешней
                           сети.
        ports (object): объект класса :class:`esu.Port`. Сеть,
                      к которой подключен данный балансировщик нагрузки
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **ESU_API_TOKEN**

    .. note:: Поля ``name``, ``vdc`` и ``port`` необходимы для
              создания.

              Поле ``name`` может быть изменено для существующего объекта.
    """
    class Meta:
        id = Field()
        name = Field()
        vdc = Field('esu.Vdc')
        floating = Field('esu.Port', allow_none=True)
        port = Field('esu.Port')

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект Lbaas по его ID

        Args:
            id (str): Идентификатор Lbaas
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект Lbaas :class:`esu.Lbaas`
        """
        dns = cls(token=token, id=id)
        dns._get_object('v1/lbaas', dns.id)
        return dns

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
        port = {
            'network': self.port.network.id,
            'fw_templates': [o2.id for o2 in self.port.fw_templates or []]
        }
        floating = None
        if self.floating:
            # keep/change or get a new IP
            floating = self.floating.id or '0.0.0.0'
        self._commit_object('v1/lbaas', name=self.name, vdc=self.vdc.id,
                            port=port, floating=floating)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/lbaas', self.id)
        self.id = None

    def get_lbaas_pool(self):
        """
        Получить список пулов балансировщика, доступных в рамках данного Lbaas.

        Returns:
            list: Список объектов :class:`esu.Vm`
        """
        if self.id is None:
            raise ObjectHasNoId

        return self._get_list(f'v1/lbaas/{self.id}/pool', LbaasPool)
