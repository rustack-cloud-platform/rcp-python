|PyPI Version| |Build Status|

===========
rustack-esu
===========

**rustack-esu** является Python библиотекой для работы с публичным облаком
`СБКлауд <https://sbcloud.ru>`_.


Установка
=========

Минимальная версия Python для установки пакета: 3.5.

.. code-block:: bash

    $ pip install rustack-esu

Примеры использования
=====================


Создание ВЦОД
-------------

.. code:: python

    from esu import Manager, Project, Vdc

    token = '72321013a102d2d3da2eaa79f0a613d40cf642fb'

    manager = Manager(token=token)
    client = manager.get_all_clients()[0]
    project = Project(name='Новый проект', client=client, token=token)
    project.create()

    hypervisor = next(h for h in project.get_available_hypervisors() \
        if h.type == 'kvm')

    vdc = Vdc(name='Новый ВЦОД', hypervisor=hypervisor, project=project,
              token=token)
    vdc.create()

    print(f'ID нового ВЦОД: {vdc.id}')

Напечатает:

.. code:: bash

    ID нового ВЦОД: 62a2df46-5412-4ca2-9d60-f6fcbe5f4b5f


Создание сервера
----------------

.. code:: python

    from esu import Manager, Project, Vdc

    vdc = Vdc.get_object('62a2df46-5412-4ca2-9d60-f6fcbe5f4b5f', token=token)
    vm = vdc.create_vm('Новый сервер', 'KVM Ubuntu 18', 'xj3$mNW11')

    print(f'ID нового сервера: {vm.id}')
    print(f'URL VNC консоли: {vm.get_vnc_url()}')  # login: ubuntu

Напечатает:

.. code:: bash

    ID нового сервера: 6c53c690-bd65-4fa5-888a-c9f8054a8ddc
    URL VNC консоли: https://...


Документация
============

Более подробную информация можно получить в
`документации <https://rustack-esu.readthedocs.io/>`_.


.. |PyPI Version| image:: https://badge.fury.io/py/rustack-esu.svg
   :target: https://badge.fury.io/py/rustack-esu
.. |Build Status| image:: https://app.travis-ci.com/pilat/rustack-esu.svg?branch=master
   :target: https://app.travis-ci.com/pilat/rustack-esu
