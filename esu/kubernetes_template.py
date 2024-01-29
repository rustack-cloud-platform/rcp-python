from esu.base import BaseAPI, Field


class KubernetesTemplate(BaseAPI):
    """
    Args:
        id (str): Идентификатор
        name (str): Имя
        min_node_cpu (int): Минимальное CPU нод
        min_node_ram (int): Минимальное RAM нод
        min_node_hdd (int): Минимальный размер диска нод
        master_template_name (string): Название шаблона мастер ноды
        node_template_name (string): Название шаблона ноды
        vm_node_visible_template (object): Объект :class:`esu.Template`
        hypervisor_type (string): Тип ресурсного пула (kvm, vmware)
    """
    class Meta:
        id = Field()
        name = Field()

    @classmethod
    def get_object(cls, id):
        """
        Получить объект шаблона по его ID

        Args:
            id (str): Идентификатор шаблона

        Returns:
            object: Возвращает объект шаблона :class:`esu.KubernetesTemplate`
        """
        template = cls(id=id)
        template._get_object('v1/kubernetes_template', template.id)
        return template
