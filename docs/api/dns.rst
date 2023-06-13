Dns
================

Доменная зона. В доменной зоне могут быть заведены DNS записи различных типов
Метод :func:`esu.Project.get_dns_zones`позволяет получить все доменные зоны
доступные в проекте.


Объект "доменная зона"
---------------------------

.. autoclass:: esu.Dns


Примеры использования
---------------------

Создать доменную зону в проекте:

.. code-block:: python

  from esu import Project, Dns

  project = Project.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  dns = Dns(project=project, name='test.com')
  dns.create()
