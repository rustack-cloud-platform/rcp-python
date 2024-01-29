from .base import BaseAPI, Field


class Subnet(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        cidr (str): CIDR
        gateway (str): Адрес шлюза
        start_ip (str): Начальный адрес для DHCP
        end_ip (str): Конечный адрес для DHCP
        enable_dhcp (bool): Включить или выключить DHCP
    """
    class Meta:
        id = Field()
        cidr = Field()
        gateway = Field()
        start_ip = Field()
        end_ip = Field()
        enable_dhcp = Field()
