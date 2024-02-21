=================
Добро пожаловать!
=================

Здесь описывается использование библиотеки rcp-python,
выполняющей роль высокоуровневой абстракции к REST API
облаков на базе Rustack Cloud Platform.



Установка
=========

.. code-block:: bash

    $ pip install rustack-esu

Начало работы
=============

Для взаимодействия с облаком через библиотеку потребуется заранее получить
токен доступа. Это можно сделать в панели управления или вызвав соответствующий
метод API.

Данный токен необходимо передавать как параметр **token** в конструкторы
объектов и в метод **get_object**. Если токен не будет передан, он будет взят
из переменной окружения **ESU_API_TOKEN**.


.. toctree::
   :caption: Управление ресурсами
   :maxdepth: 1

   api/manager
   api/client
   api/project
   api/hypervisor
   api/vdc


.. toctree::
   :caption: Вычислительные ресурсы
   :maxdepth: 1

   api/vm
   api/template
   api/template_field
   api/vm_metadata
   api/kubernetes
   api/kubernetes_template
   api/paas_service
   api/paas_template


.. toctree::
   :caption: Хранение данных
   :maxdepth: 1

   api/disk
   api/storage_profile
   api/s3
   api/s3_bucket


.. toctree::
   :caption: Резервное копирование, снапшоты и образы
   :maxdepth: 1

   api/backup
   api/image
   api/snapshot


.. toctree::
   :caption: Сеть, маршрутизация, доменные зоны
   :maxdepth: 1

   api/network
   api/subnet
   api/router
   api/port
   api/firewall_template
   api/firewall_template_rule
   api/dns
   api/dns_record

.. toctree::
   :caption: CHANGELOG
   :maxdepth: 2

   changelog/0.1.6.rst
