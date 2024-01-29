from rcp.api.subnet import Subnet


class SubnetMixin:

    @classmethod
    def subnet_create(cls, cidr: str, gateway: str, start_ip: str,
                      end_ip: str, enable_dhcp: bool) -> Subnet:
        """
        Args:
            cidr (str): CIDR
            gateway (str): Адрес шлюза
            start_ip (str): Начальный адрес для DHCP
            end_ip (str): Конечный адрес для DHCP
            enable_dhcp (bool): Включить или выключить DHCP
        """
        return Subnet(cidr=cidr, gateway=gateway, start_ip=start_ip,
                      end_ip=end_ip, enable_dhcp=enable_dhcp)
