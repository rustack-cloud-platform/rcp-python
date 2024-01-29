from esu.base import BaseAPI, Field, FieldList, ObjectAlreadyHasId, \
    ObjectHasNoId


class LbaasPoolMember(BaseAPI):
    """
    Args:
        port (str): Порт участника пула балансировщика
        vm (object): Объект :class:`esu.Vm`
        weight (str): Вес участника пула балансировщика
    """
    class Meta:
        port = Field()
        vm = Field('esu.Vm')
        weight = Field()


class LbaasPool(BaseAPI):
    """
    Args:
        id (str): Идентификатор Lbaas Pool
        name (str): Имя Lbaas Pool
        lbaas (object): Объект класса :class:`esu.Lbaas`. Балансировщик, к
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

    .. note:: Поля ``members`` и ``port`` необходимы для
              создания.

    """
    class Meta:
        id = Field()
        name = Field()
        lbaas = Field('esu.Lbaas')
        connlimit = Field()
        cookie_name = Field()
        members = FieldList(LbaasPoolMember)
        method = Field()
        port = Field()
        protocol = Field()
        session_persistence = Field()

    @classmethod
    def get_object(cls, lbaas, pool_id):
        """
        Получить объект пула балансировщика по его ID

        Args:
            lbaas :class:`esu.Lbaas`
            pool_id (str): Идентификатор Lbaas Pool

        Returns:
            object: Возвращает объект LbaasPool :class:`esu.LbaasPool`
        """
        pool = cls(id=pool_id, lbaas=lbaas)
        pool._get_object('v1/lbaas/{}/pool'.format(pool.lbaas.id), pool.id)
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
        pull = {
            'members': members,
            'method': self.method,
            'port': self.port,
            'protocol': self.protocol,
            'session_persistence': self.session_persistence,
            'name': self.name,
        }
        if self.connlimit is not None:
            pull['connlimit'] = self.connlimit
        if self.cookie_name is not None:
            pull['cookie_name'] = self.cookie_name

        self._commit_object('v1/lbaas/{}/pool'.format(self.lbaas.id), **pull)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/lbaas/{}/pool'.format(self.lbaas.id), self.id)
        self.id = None
