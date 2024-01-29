from .base import BaseAPI, Field


class Hypervisor(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        type (str): Тип гипервизора. vmware или kvm
    """
    class Meta:
        id = Field()
        name = Field()
        type = Field()
