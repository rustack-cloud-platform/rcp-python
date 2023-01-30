from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId


class LbaasPool(BaseAPI):
    """
    Args:
        id (str): Идентификатор Lbaas Pool
        name (str): Имя Lbaas Pool
        lbaas_id (object): Объект класса :class:`esu.Lbaas`. Проект, к
                          которому относится данный Lbaas Pool
        connlimit (str): лимит соединений  для пула балансировщика
        cookie_name (str): Имя cookie
        members (list): Список объектов класса :class:`esu.LbaasPoolMember`.
                          Список участников, которые подключены к данному
                          пулу балансировщика нагрузки
        method (str): метод по которому будет работать пул балансировщика
        port (str): порт по которому будет подключаться пул балансировщика
        protocol (str): протокол по которому будет работать пул балансировщика
        session_persistence (str): лимит соединений для пула балансировщика
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **ESU_API_TOKEN**

    .. note:: Поля ``members`` и ``port`` необходимы для
              создания.

    """
    class Meta:
        id = Field()
        name = Field()
        lbaas_id = Field('esu.Project')
        connlimit = Field('esu.Project')
        cookie_name = Field('esu.Project')
        members = FieldList('esu.LbaasPoolMember')
        method = Field('esu.Project')
        port = Field('esu.Project')
        protocol = Field('esu.Project')
        session_persistence = Field('esu.Project')

    @classmethod
    def get_object(cls, lbaas_id, pool_id, token=None):
        """
        Получить объект пула балансировщика по его ID

        Args:
            id (str): Идентификатор Lbaas Pool
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект LbaasPool :class:`esu.LbaasPool`
        """
        pool = cls(token=token, id=pool_id, lbaas_id=lbaas_id)
        pool._get_object(f'v1/lbaas/{pool.lbaas_id}/pool', pool.id)
        return pool

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
        members = [{
            'port': o.port,
            'vm': o.vm.id,
            'weight': o.weight
        } for o in self.members]

        self._commit_object(
            f'v1/lbaas/{self.lbaas_id}/pool',
            connlimit=self.connlimit,
            members=members,
            cookie_name=self.cookie_name,
            method=self.method,
            port=self.port,
            protocol=self.protocol,
            session_persistence=self.session_persistence,
            name=self.name,
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

        self._destroy_object(f'v1/lbaas/{self.lbaas_id}/pool', self.id)
        self.id = None
