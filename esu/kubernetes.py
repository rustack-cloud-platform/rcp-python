from esu.base import BaseAPI, Field, ObjectAlreadyHasId, ObjectHasNoId


class Kubernetes(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        node_cpu (int): CPU нод
        node_ram (int): RAM нод
        node_disk_size (int): Размер диска нод
        node_storage_profile (object): Объект :class:`esu.StorageProfile`
        nodes_count (int): Количество нод в кластере
        vdc (object): Объект класса :class:`esu.Vdc`. ВЦОД, к которому
                  относится данный кластер
        template (str): Идентификатор шаблона Kubernetes
        user_public_key (string): публичный SSH ключ
        floating (object): Объект класса :class:`esu.Port`. 
                    Порт подключения кластера к внешней сети.
                    Если None, кластер не имеет подключения к внешней сети.
        """
    class Meta:
        id = Field()
        name = Field()
        node_cpu = Field()
        node_ram = Field()
        node_disk_size = Field()
        node_storage_profile = Field('esu.StorageProfile')
        nodes_count = Field()
        template = Field('esu.KubernetesTemplate')
        user_public_key = Field()
        vdc = Field('esu.Vdc')
        floating = Field('esu.Port', allow_none=True)

    @classmethod
    def get_object(cls, id, token=None):
        """
        Получить объект kubernetes по его ID

        Args:
            id (str): Идентификатор Kubernetes
            token (str): Токен для доступа к API. Если не передан, будет
                         использована переменная окружения **ESU_API_TOKEN**

        Returns:
            object: Возвращает объект кластера kubernetes :class:`esu.Kubernetes`
        """
        k8s = cls(token=token, id=id)
        k8s._get_object('v1/kubernetes', k8s.id)

        return k8s

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
        """
        if self.id is None:
            raise ObjectHasNoId

        self._commit()
        return self

    def _commit(self):
        k8s = {
            'vdc': self.vdc.id,
            'template': self.template.id,
            'name': self.name,
            'node_cpu': self.node_cpu,
            'node_ram': self.node_ram,
            'node_disk_size': self.node_disk_size,
            'node_storage_profile': self.node_storage_profile.id,
            'nodes_count': self.nodes_count,
            'user_public_key': self.user_public_key
        }
        floating = None
        if self.floating:
            # keep/change or get a new IP
            floating = self.floating.id or '0.0.0.0'
        k8s['floating'] = floating

        self._commit_object('v1/kubernetes', **k8s)

    def destroy(self):
        """
        Удалить объект

        Raises:
            ObjectHasNoId: Когда производится попытка удалить несуществующий
                           объект
        """
        if self.id is None:
            raise ObjectHasNoId

        self._destroy_object('v1/kubernetes', self.id)
        self.id = None

    def get_dashbord_url(self):
        """
        Получить ссылку на Dashboard для открытия консоли k8s

        Returns:
            str: Адрес дашборда
        """
        url = self._call('GET', 'v1/kubernetes/{}/dashboard'.format(self.id))
        uri = url['url']
        return '{}{}'.format(self.endpoint_url, uri)
