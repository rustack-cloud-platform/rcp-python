Vm
==

Виртуальный (выделенный) сервер эмулирует работу отдельного физического
сервера. Сервер может быть создан с операционной системой семейства Linux или
Windows, может иметь несколько сетевых подключений и дисков.


Объект "виртуальный сервер"
---------------------------

.. autoclass:: esu.Vm


Примеры использования
---------------------

.. _example-2:

Создать виртуальный сервер на базе ОС Ubuntu 18:

.. code-block:: python

  from requests import HTTPError
  from esu import Manager, VmMetadata, Port, Disk, Vm

  vdc = Manager().get_all_vdcs()[0]  # Первый доступный пользователю ВЦОД
  network = next(n for n in vdc.get_networks() if n.is_default)  # Сеть по умолчанию
  template = next(v for v in vdc.get_templates() if 'Ubuntu 18' in v.name)  # Шаблон ОС
  storage_profile = vdc.get_storage_profiles()[0]  # Первый доступный профиль хранения
  firewall_template = next(f for f in vdc.get_firewall_templates() if f.name == 'По-умолчанию')  # Разрешить исходящие подключения
  password = 'nw9fH4n$11'  # Пароль для виртуального сервера

  metadata = []
  for field in template.get_fields():
      value = field.default
      if field.system_alias == 'password':
          value = password
      metadata.append(VmMetadata(field=field, value=value))

  port = Port(network=network, fw_templates=[firewall_template])
  disk = Disk(name='Системный диск', size=15, storage_profile=storage_profile)

  vm = Vm(name='Новый сервер', cpu=2, ram=2, vdc=vdc, template=template,
          metadata=metadata, ports=[port], disks=[disk])

  try:
      vm.create()
  except HTTPError as ex:
      api_answer = ex.response.json()
      print(f'Error has happend: {api_answer}')
  


Назначить случайный плавающий IP адрес на существующий виртуальный сервер:

.. code-block:: python

  from esu import Vm, Port

  vm = Vm.get_object('954fd467-fd9a-4ce7-b4df-1e81e557bce9')
  vm.floating = Port()
  vm.save()
