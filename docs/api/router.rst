Router
=======

Маршрутизаторы управляют связностью приватных сетей с интернетом. Маршрутизатор
может иметь собственный публичный адрес, тогда все виртуальные машины будут
выходить в Интернет через этот IP-адрес, если на них не назначен собственный
плавающий IP.

Объект "маршрутизатор"
----------------------

.. autoclass:: esu.Router


Примеры использования
---------------------

Создать новый маршрутизатор и подключить его к первой сети во ВЦОДе:

.. code-block:: python

  from esu import Vdc, Port, Router

  vdc = Vdc.get_object('e5d9a192-c5da-485a-b134-1b14ec9c57d9')
  network = vdc.get_networks()[0]
  port = Port(network=network)
  router = Router(vdc=vdc, name='Новый маршрутизатор', ports=[port])
  router.create()

Подключить определенный маршрутизатор к существующей сети:

.. code-block:: python

  from esu import Router, Network, Port

  router = Router.get_object('58385696-32c6-4a5c-bafe-895815eedf04')
  network = Network.get_object('b9e6df93-0d04-4dac-a3c1-1a8539b8e445')
  Port(network=network, device=router).create()
