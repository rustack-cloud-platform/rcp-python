from bcc.base import BaseAPI


class Manager(BaseAPI):
    """
    Args:
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **BCC_API_TOKEN**,
        endpoint_url (str): Адрес API. Если не передан, будет
                     использована переменная окружения **BCC_API_URL**
    """
    class Meta:
        pass

    def get_all_clients(self):
        """
        Возвращает список объектов всех доступных пользователю клиентов. Если
        текущему пользователю был предоставлен доступ к еще одному клиенту,
        данный список будет содержать два элемента.

        Returns:
            list: Список объектов :class:`bcc.Client`
        """
        return self._get_list('v1/client', 'bcc.Client')

    def get_all_projects(self):
        """
        Возвращает список объектов всех доступных пользователю проектов. Если
        текущий пользователь имеет несколько проектов или ему предоставили
        доступ к стороннему проекту, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`bcc.Project`
        """
        return self._get_list('v1/project', 'bcc.Project')

    def get_all_vdcs(self):
        """
        Возвращает список объектов всех доступных пользователю ВЦОДов. Если
        текущий пользователь имеет несколько ВЦОДов или ему был предоставлен
        доступ к сотронним проектам, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`bcc.Vdc`
        """
        return self._get_list('v1/vdc', 'bcc.Vdc')

    def get_all_vms(self):
        """
        Возвращает список объектов всех доступных пользователю виртуальных
        выделенных серверов. Если текущий пользователь имеет несколько
        виртуальных серверов или ему был предоставлен доступ к
        сторонним проектам, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`bcc.Vm`
        """
        return self._get_list('v1/vm', 'bcc.Vm')

    def get_all_storage_profiles(self):
        """
        Возвращает список объектов всех доступных пользователю профилей
        хранения.

        Returns:
            list: Список объектов :class:`bcc.StorageProfile`
        """
        return self._get_list('v1/storage_profile', 'bcc.StorageProfile')

    def get_all_platforms(self):
        """
        Возвращает список объектов всех доступных пользователю платформ.

        Returns:
            list: Список объектов :class:`bcc.Platform`
        """
        return self._get_list('v1/platform', 'bcc.Platform', with_pages=False)

    def get_all_firewall_templates(self):
        """
        Возвращает список объектов всех доступных пользователю шаблонов
        брандмауэра.

        Returns:
            list: Список объектов :class:`bcc.FirewallTemplate`
        """
        return self._get_list('v1/firewall', 'bcc.FirewallTemplate')

    def get_all_networks(self):
        """
        Возвращает список объектов всех доступных пользователю сетей.

        Returns:
            list: Список объектов :class:`bcc.Network`
        """
        return self._get_list('v1/network', 'bcc.Network')

    def get_all_paas_services(self):
        """
        Возвращает список объектов всех доступных пользователю PaaS сервисов.

        Returns:
            list: Список объектов :class:`bcc.PaasService`
        """
        return self._get_list('v1/paas_service', 'bcc.PaasService')
