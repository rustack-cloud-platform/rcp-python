from rcp.mixins.project_mixin import ProjectMixin
from rcp.mixins.vdc_mixin import VdcMixin
from rcp.mixins.client_mixin import ClientMixin
from rcp.mixins.storage_profile_mixin import StorageProfileMixin
from rcp.mixins.disk_mixin import DiskMixin
from rcp.mixins.network_mixin import NetworkMixin
from rcp.mixins.subnet_mixin import SubnetMixin
from rcp.mixins.router_mixin import RouterMixin
from rcp.mixins.port_mixin import PortMixin


class RCPManager(ProjectMixin, VdcMixin, ClientMixin, StorageProfileMixin, DiskMixin,
                 NetworkMixin, SubnetMixin, RouterMixin, PortMixin):
    pass
    # """
    # Args:
    #     token (str): Токен для доступа к API. Если не передан, будет
    #                  использована переменная окружения **ESU_API_TOKEN**
    #     endpoint_url (str): Доменное имя стенда. Если не передано, будет
    #                         использована переменная окружения **ESU_API_URL**
    #     test_mode (bool): Включение тестового режима работы библиотеки
    # """
    # def __init__(self, *args, **kwargs):
    #     self.project = rcp.Project()
    #     self.vdc = rcp.Vdc()
    #     # self.client = rcp.Client()
    #     self.disk = rcp.Disk()
    #     # self.dns = rcp.Dns()
    #     # self.dns_record = rcp.DnsRecord()
    #     # self.firewall_template = rcp.FirewallTemplate()
    #     # self.firewall_template_rule = rcp.FirewallTemplateRule()
    #     # self.hypervisor = rcp.Hypervisor()
    #     # self.image = rcp.Image()
    #     # self.kubernetes = rcp.Kubernetes()
    #     # self.kubernetes_template = rcp.KubernetesTemplate()
    #     # self.lbaas = rcp.Lbaas()
    #     # self.lbaas_pool = rcp.LbaasPool()
    #     # self.network = rcp.Network()
    #     # self.paas_service = rcp.PaasService()
    #     # self.paas_template = rcp.PaasTemplate()
    #     # self.platform = rcp.Platform()
    #     # self.port = rcp.Port()
    #     # self.port_forwarding = rcp.PortForwarding()
    #     # self.port_forwarding_rule = rcp.PortForwardingRule()
    #     # self.public_key = rcp.PublicKey()
    #     # self.router = rcp.Router()
    #     # self.router_firewall_rule = rcp.RouterFirewallRule()
    #     # self.router_port_forwarding = rcp.RouterPortForwarding()
    #     # self.router_route = rcp.RouterRoute()
    #     # self.s3 = rcp.S3()
    #     # self.s3_bucket = rcp.S3Bucket()
    #     # self.snapshot = rcp.Snapshot()
    #     # self.storage_profile = rcp.StorageProfile()
    #     # self.subnet = rcp.Subnet()
    #     # self.template = rcp.Template()
    #     # self.template_field = rcp.TemplateField()
    #     # self.user = rcp.User()
    #     self.vm = rcp.Vm()
    #     # self.vm_metadata = rcp.VmMetadata()
    #
    # class Meta:
    #     pass
    #
    # def get_all_clients(self):
    #     """
    #     Возвращает список объектов всех доступных пользователю клиентов. Если
    #     текущему пользователю был предоставлен доступ к еще одному клиенту,
    #     данный список будет содержать два элемента.
    #
    #     Returns:
    #         list: Список объектов: class:`rcp.Client`
    #     """
    #     return self._get_list('v1/client', 'rcp.Client')
