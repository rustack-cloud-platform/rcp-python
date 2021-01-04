Disk
====

Диск является сущностью для хранения информации. Диск нельзя создать отдельно
от виртуального сервера. Чтобы создать диск, следует использовать метод
:func:`esu.Vm.add_disk` у уже существующего сервера.

В то же время, уже созданный диск может быть от него отключен и подключен
позднее к другому виртуальному серверу или удален.

Можно изменять размер существующего диска в сторону увеличения.


Объект "диск"
-------------

.. autoclass:: esu.Disk

Примеры использования
---------------------

Добавить диск типа SATA к уже существующему виртуальному серверу:

.. code-block:: python

  from esu import Vm, Disk

  vm = Vm.get_object('954fd467-fd9a-4ce7-b4df-1e81e557bce9')

  storage_profile = next(p for p in vm.vdc.get_storage_profiles() \
      if p.name == 'SATA')
  disk = Disk(name='Дополнительный диск', size=30,
              storage_profile=storage_profile)

  vm.add_disk(disk)


Увеличить диск виртуального сервера:

.. code-block:: python

  from esu import Vm

  vm = Vm.get_object('954fd467-fd9a-4ce7-b4df-1e81e557bce9')
  disk = vm.disks[0]
  disk.size += 5
  disk.save()