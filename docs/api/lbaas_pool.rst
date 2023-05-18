LbaasPool
================

Балансировщик нагрузки - позволяет балансировать трафик между серверами.
В балансировщик нагрузки добавляют пулы балансировки с различными алгоритмами
балансировки в которые добавляются участники - серверы.



Объект "пул балансировщика нагрузки"
---------------------------

.. autoclass:: esu.LbaasPool


Примеры использования
---------------------

Создать балансировщик нагрузки:

.. code-block:: python

  from esu import Lbaas, LbaasPool, LbaasPoolMember, Vm

  lbaas = Lbaas.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vm1 = Vm.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vm2 = Vm.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745g5')
  pool_member1 = LbaasPoolMember(vm=vm1, weight=50, port=80)
  pool_member2 = LbaasPoolMember(vm=vm2, weight=50, port=80)
  lbaas_pool = LbaasPool(method="ROUND_ROBIN", port=80, protocol="HTTP",
                         members=[pool_member1, pool_member2], lbaas=lbaas)
  lbaas_pool.create()