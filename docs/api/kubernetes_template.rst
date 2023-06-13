KubernetesTemplate
================

Шаблон кластера Kubernetes - необходим для создания кластера Kubernetes.
Список шаблонов кластера Kubernetes доступных для созданного ВЦОД можно
получить используя метод :func:`esu.Vdc.get_k8s_templates`


Объект "шаблон кластера kubernetes"
---------------------------

.. autoclass:: esu.KubernetesTemplate


Примеры использования
---------------------

Запросить список шаблонов кластера kubernetes во ВЦОД:

.. code-block:: python

  from esu import Vdc

  vdc = Vdc.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  k8s_templates = vdc.get_k8s_templates()