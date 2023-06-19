PortForwardingRule
=======

Правило перенаправление портов. Используется для того, чтобы по IP адресу по определённому
порту попадать на порт сервера для которого настроено перенаправление. Указывается порт
устройства с которого должны быть доступны порты сервера, протокол для которого
настраивается перенаправление, а также подключение сервера на которое будет
осуществляться перенаправление.
Такое перенаправление портов создаётся на отдельно зарезервированном публичном IP
адресе :func:`esu.Port.create_fip`

Функционал создания такого перенаправления портов доступен только для
ресурсного пула под управлением Openstack.

Объект "Правило перенаправления портов"
----------------------

.. autoclass:: esu.PortForwardingRule


Примеры использования
---------------------

Создать новое правило перенаправления портов:

.. code-block:: python

  from esu import Port, PortForwarding, PortForwardingRule

  port_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
  port = Port.get_object(port_id)
  port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
  port_forwarding = PortForwarding.get_object(port_forwarding_id)
  p_f_rule = PortForwardingRule(port_forwarding=port_forwarding,
                                internal_port=80, external_port=80,
                                protocol="tcp", port=port)
  p_f_rule.create()
