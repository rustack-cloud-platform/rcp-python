Backup
=======

Задача резервного копирования - создаётся для сервера или для нескольких серверов.
Для создания задачи требуется указать расписание: дни и время выполнения задачи, а
также серверы для которых она будет выполняться.
В каждой задаче резервного копирования хранятся точки восстановления сервера. Из
точек восстановления можно восстановить сервер в состояние сохранённое в точке.


Объект "задача резервного копирования"
---------------

.. autoclass:: esu.Backup


Примеры использования
---------------------

Создать задачу резервного копирования для сервера:

.. code-block:: python

  from esu import Vm, Backup, Vdc

  vdc = Vdc.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vm = Vm.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  backup = Backup(name="Test_Backup", vdc=vdc, vms=[vm], week_days=[1, 2],
                  time="09:00:00", retain_cycles=2)


Немедленно запустить выполнение задачи - создать точку восстановления:

.. code-block:: python

  import requests
  from esu import Backup

  backup = Backup.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  backup.start_immediately()


Восстановить сервер из точки восстановления:

.. code-block:: python

  from esu import Vm, Backup

  backup = Backup.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vm = Vm.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  restore_point = backup.get_restore_points()[0]  # Первая доступная точка восстановления
  backup.restore(vm=vm, restore_point=restore_point)
