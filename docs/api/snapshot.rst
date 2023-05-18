Snapshot
=======

Объект снапшота. Снапшот - слепок состояния системы,
который можно использовать для последующего восстановления сервера в сохранённое
в снапшоте состояние


Объект "снапшот"
---------------

.. autoclass:: esu.Snapshot


Примеры использования
---------------------

Создать снапшот для определённого сервера:

.. code-block:: python

  from esu import Vm, Snapshot

  vm = Vm.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  snapshot = Snapshot(vm=vm, name='Новый снапшот')
  snapshot.create()


Восстановить сервер из снапшота:

.. code-block:: python

  from esu import Vm, Snapshot

  snapshot = Snapshot.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vm = Vm.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vm.revert(snapshot=snapshot)