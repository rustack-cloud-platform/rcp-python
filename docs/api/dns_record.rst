DnsRecord
================

Запись доменной зоны. В доменной зоне могут быть заведены DNS записи
различных типов


Объект "запись доменной зоны"
---------------------------

.. autoclass:: esu.DnsRecord


Примеры использования
---------------------

Создать запись доменной зоны в доменной зоне:

.. code-block:: python

  from esu import Dns, DnsRecord

  dns = Dns.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  record = DnsRecord(type="A", host="host", data="10.0.1.1",
                     dns=dns, ttl=86400)
  record.create()