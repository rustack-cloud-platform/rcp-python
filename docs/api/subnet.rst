Subnet
======

Подсеть позволяет задать диапазоны IP-адресов, доступные для использования
устройствами, подключенными к определенной сети.

Подсеть не может быть создана или удалена как самостоятельная
сущность. Следует использовать методы :func:`esu.Network.add_subnet` и
:func:`esu.Network.remove_subnet` у уже существующей сети.

Объект "подсеть"
----------------

.. autoclass:: esu.Subnet


Примеры использования
---------------------

Создание сети с Subnet:

.. code-block:: python

  from esu import Network, Subnet

  subnet = Subnet(cidr='10.22.23.0/24', gateway='10.22.23.1',
                  start_ip='10.22.23.2', end_ip='10.22.23.254',
                  enable_dhcp=True)

  network = Network(name='Network 1', subnets=[subnet])
  network.create()

Добавление Subnet к уже существующей сети:

.. code-block:: python

  from esu import Network, Subnet

  network = Network.get_object('b9e6df93-0d04-4dac-a3c1-1a8539b8e445')
  subnet = Subnet(cidr='10.22.23.0/24', gateway='10.22.23.1',
                  start_ip='10.22.23.2', end_ip='10.22.23.254',
                  enable_dhcp=True)

  network.add_subnet(subnet)
