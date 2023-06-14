RouterFirewallRule
=======

Правило брандмауэра на роутере. Правило может быть создано как для отдельного сервера, который
подключен к роутеру, так и для подсети к которой подключен роутер (адрес и порты).

Функционал создания правил брандмауэра на роутере доступен только для ресурсного пула
под управлением VMware.

Объект "Правило брандмауэра на роутере"
----------------------

.. autoclass:: esu.RouterFirewallRule


Примеры использования
---------------------

Создать новое правило брандмауэра на роутере:

.. code-block:: python

  from esu import Router, RouterFirewallRule

  router = Router.get_object('58385696-32c6-4a5c-bafe-895815eedf04')
  fw_rule = RouterFirewallRule(name="Rule", protocol="tcp", router=router,
                               direction="ingress", source_ip="10.0.1.0/24",
                               src_port_range_min=80, src_port_range_max=90,
                               dst_port_range_min=80, dst_port_range_max=90)
  fw_rule.create()

