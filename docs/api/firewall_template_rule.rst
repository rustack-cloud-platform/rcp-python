FirewallTemplateRule
================

Правило шаблона брандмауэра. Правила добавляются в уже созданный
шаблон брандмауэра


Объект "правило шаблона брандмауэра"
---------------------------

.. autoclass:: esu.FirewallTemplateRule


Примеры использования
---------------------
Создать правило для шаблона брандмауэра:

.. code-block:: python

  from esu import FirewallTemplate, FirewallTemplateRule

  fw_template = FirewallTemplate.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  firewall_rule = QAFirewallRule(firewall=fw_template, name="Rule",
                                 direction="egress", protocol="tcp",
                                 destination_ip="0.0.0.0/0")
  firewall_rule.create
