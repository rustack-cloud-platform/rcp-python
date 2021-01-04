Project
=======

Объект проекта. Проекты представляют из себя логические сущности, в которые
объединены те или иные облачные услуги. Проекты могут создаваться
клиентами, а после регистрации всегда существует проект по умолчанию.


Объект "проект"
---------------

.. autoclass:: esu.Project


Примеры использования
---------------------

Создать проект на определенном клиенте:

.. code-block:: python

  from esu import Client, Project

  client = Client.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  project = Project(client=client, name='Новый проект')
  project.create()


Переименовать первый проект на клиенте:

.. code-block:: python

  from esu import Client, Project

  client = Client.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  project = client.get_projects()[0]
  project.name = 'Новое имя проекта'
  project.save()
