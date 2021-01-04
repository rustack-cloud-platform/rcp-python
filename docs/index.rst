=================
Добро пожаловать!
=================

Данная документация описывает использование библиотеки **rustack-esu**,
выполняющей роль высокоуровневой абстракции к REST API облака
гиперконвергентного решения РУСТЭК-ЕСУ. Описание методов API можно найти в
`отдельной документации <https://cp.sbcloud.ru/swagger/>`_.


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
   api/vdc


.. toctree::
   :caption: Вычислительные ресурсы
   :maxdepth: 1

   api/vm
   api/template
   api/template_field
   api/vm_metadata


.. toctree::
   :caption: Хранение данных
   :maxdepth: 1

   api/disk
   api/storage_profile


.. toctree::
   :caption: Сеть и маршрутизация
   :maxdepth: 1

   api/network
   api/subnet
   api/router
   api/port
   api/firewall_template
