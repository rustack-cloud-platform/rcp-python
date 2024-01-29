import rcp
from rcp.base import BaseAPI


class RCPManager(BaseAPI):
    """
    Args:
        token (str): Токен для доступа к API. Если не передан, будет
                     использована переменная окружения **ESU_API_TOKEN**
        endpoint_url (str): Доменное имя стенда. Если не передано, будет
                            использована переменная окружения **ESU_API_URL**
        test_mode (bool): Включение тестового режима работы библиотеки
    """

    def __init__(self, *args, **kwargs):
        self.project = rcp.Project()
        self.vdc = rcp.Vdc()
        # self.client = rcp.Client()
        # self.disk = rcp.Disk()
        # self.dns = rcp.Dns()
        # self.dns_record = rcp.DnsRecord()
        # self.firewall_template = rcp.FirewallTemplate()
        # self.firewall_template_rule = rcp.FirewallTemplateRule()
        # self.hypervisor = rcp.Hypervisor()
        # self.image = rcp.Image()
        # self.kubernetes = rcp.Kubernetes()
        # self.kubernetes_template = rcp.KubernetesTemplate()
        # self.lbaas = rcp.Lbaas()
        # self.lbaas_pool = rcp.LbaasPool()
        # self.network = rcp.Network()
        # self.paas_service = rcp.PaasService()
        # self.paas_template = rcp.PaasTemplate()
        # self.platform = rcp.Platform()
        # self.port = rcp.Port()
        # self.port_forwarding = rcp.PortForwarding()
        # self.port_forwarding_rule = rcp.PortForwardingRule()
        # self.public_key = rcp.PublicKey()
        # self.router = rcp.Router()
        # self.router_firewall_rule = rcp.RouterFirewallRule()
        # self.router_port_forwarding = rcp.RouterPortForwarding()
        # self.router_route = rcp.RouterRoute()
        # self.s3 = rcp.S3()
        # self.s3_bucket = rcp.S3Bucket()
        # self.snapshot = rcp.Snapshot()
        # self.storage_profile = rcp.StorageProfile()
        # self.subnet = rcp.Subnet()
        # self.template = rcp.Template()
        # self.template_field = rcp.TemplateField()
        # self.user = rcp.User()
        self.vm = rcp.Vm()
        # self.vm_metadata = rcp.VmMetadata()

    class Meta:
        pass

    def get_all_clients(self):
        """
        Возвращает список объектов всех доступных пользователю клиентов. Если
        текущему пользователю был предоставлен доступ к еще одному клиенту,
        данный список будет содержать два элемента.

        Returns:
            list: Список объектов: class:`rcp.Client`
        """
        return self._get_list('v1/client', 'rcp.Client')

    def get_all_projects(self):
        """
        Возвращает список объектов всех доступных пользователю проектов. Если
        текущий пользователь имеет несколько проектов или ему предоставили
        доступ к стороннему проекту, данный список будет содержать их все.

        Returns:
            list: Список объектов: class:`rcp.Project`
        """
        return self._get_list('v1/project', 'rcp.Project')

    def get_all_vdcs(self):
        """
        Возвращает список объектов всех доступных пользователю ВЦОДов. Если
        текущий пользователь имеет несколько ВЦОДов или ему был предоставлен
        доступ к сторонним проектам, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`rcp.Vdc`
        """
        return self._get_list('v1/vdc', 'rcp.Vdc')

    def get_all_vms(self):
        """
        Возвращает список объектов всех доступных пользователю виртуальных
        выделенных серверов. Если текущий пользователь имеет несколько
        виртуальных серверов или ему был предоставлен доступ к
        сторонним проектам, данный список будет содержать их все.

        Returns:
            list: Список объектов :class:`rcp.Vm`
        """
        return self._get_list('v1/vm', 'rcp.Vm')

    def get_all_storage_profiles(self):
        """
        Возвращает список объектов всех доступных пользователю профилей
        хранения.

        Returns:
            list: Список объектов :class:`rcp.StorageProfile`
        """
        return self._get_list('v1/storage_profile', 'rcp.StorageProfile')

    def get_all_platforms(self):
        """
        Возвращает список объектов всех доступных пользователю платформ.

        Returns:
            list: Список объектов :class:`rcp.Platform`
        """
        return self._get_list('v1/platform', 'rcp.Platform', with_pages=False)

    def get_all_firewall_templates(self):
        """
        Возвращает список объектов всех доступных пользователю шаблонов
        брандмауэра.

        Returns:
            list: Список объектов :class:`rcp.FirewallTemplate`
        """
        return self._get_list('v1/firewall', 'rcp.FirewallTemplate')

    def get_all_networks(self):
        """
        Возвращает список объектов всех доступных пользователю сетей.

        Returns:
            list: Список объектов :class:`rcp.Network`
        """
        return self._get_list('v1/network', 'rcp.Network')

    def get_all_paas_services(self):
        """
        Возвращает список объектов всех доступных пользователю PaaS сервисов.

        Returns:
            list: Список объектов :class:`rcp.PaasService`
        """
        return self._get_list('v1/paas_service', 'rcp.PaasService')
