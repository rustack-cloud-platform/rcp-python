Vdc
===

Объект виртуального центра обработки данных (ВЦОД). ВЦОДы включают в себя
ИТ-инфраструктуру, вычислительные ресурсы и ресурсы для хранения информации.

При создании ВЦОД автоматически создаются сеть :class:`esu.Network` и
маршрутизатор :class:`esu.Router`, которые не могут быть удалены.

Поддерживается два типа гипервизора: **VMware vSphere ESXi** и
**OpenStack KVM**.


Объект "ВЦОД"
-------------

.. autoclass:: esu.Vdc


Примеры использования
---------------------

.. _example-3:

Создание нового ВЦОД VMware в первом доступном пользователю проекте:

.. code-block:: python

  from esu import Manager, Vdc

  project = Manager().get_all_projects()[0]
  hypervisor = next(h for h in project.get_available_hypervisors() \
        if h.type == 'vmware')

  vdc = Vdc(name='Новый ВЦОД', hypervisor=hypervisor, project=project)
  vdc.create()

.. _example-1:

Вывести на экран список доступных в определенном ВЦОДе шаблонов операционных
систем:

.. code-block:: python

  from esu import Manager, Vdc

  project = Manager().get_all_projects()[0]
  vdc = Vdc.get_object('e5d9a192-c5da-485a-b134-1b14ec9c57d9')
  for template in vdc.get_templates():
      print(template.name)
