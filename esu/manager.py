from esu.base import BaseAPI


class Manager(BaseAPI):
    """
    Args:
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **ESU_API_TOKEN**
    """
    class Meta:
        pass

    def get_all_clients(self):
        """
        Возвращает список объектов всех доступных пользователю клиентов. Если
        текущему пользователю был предоставлен доступ к еще одному клиенту,
        данный список будет содержать два элемента.

        Returns:
            list: Список объектов :class:`esu.Client`
        """
        return self._get_list('v1/client', 'esu.Client')

    def get_all_projects(self):
        """
        Возвращает список объектов всех доступных пользователю проектов. Если
        текущий пользователь имеет несколько проектов или ему предоставили
        доступ к стороннему проекту, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`esu.Project`
        """
        return self._get_list('v1/project', 'esu.Project')

    def get_all_vdcs(self):
        """
        Возвращает список объектов всех доступных пользователю ВЦОДов. Если
        текущий пользователь имеет несколько ВЦОДов или ему был предоставлен
        доступ к сотронним проектам, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`esu.Vdc`
        """
        return self._get_list('v1/vdc', 'esu.Vdc')

    def get_all_vms(self):
        """
        Возвращает список объектов всех доступных пользователю виртуальных
        выделенных серверов. Если текущий пользователь имеет несколько
        виртуальных серверов или ему был предоставлен доступ к
        сторонним проектам, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`esu.Vm`
        """
        return self._get_list('v1/vm', 'esu.Vm')

    def get_all_storage_profiles(self):
        """
        Возвращает список объектов всех доступных пользователю профилей
        хранения.

        Returns:
            list: Список объектов :class:`esu.StorageProfile`
        """
        return self._get_list('v1/storage_profile', 'esu.StorageProfile')

    def get_all_platforms(self):
        """
        Возвращает список объектов всех доступных пользователю платформ.

        Returns:
            list: Список объектов :class:`esu.Platform`
        """
        return self._get_list('v1/platform', 'esu.Platform', with_pages=False)

    def get_all_firewall_templates(self):
        """
        Возвращает список объектов всех доступных пользователю шаблонов
        брандмауэра.

        Returns:
            list: Список объектов :class:`esu.FirewallTemplate`
        """
        return self._get_list('v1/firewall', 'esu.FirewallTemplate')

    def get_all_networks(self):
        """
        Возвращает список объектов всех доступных пользователю сетей.

        Returns:
            list: Список объектов :class:`esu.Network`
        """
        return self._get_list('v1/network', 'esu.Network')
