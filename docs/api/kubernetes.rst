Kubernetes
================

Кластер Kubernetes. Kubernetes — открытое программное обеспечение для
оркестрации контейнеризированных приложений — автоматизации их развёртывания,
масштабирования и координации в условиях кластера. Кластер состоит из нескольких
серверов - нод. Существует мастер-нода, главная управляющая нода кластера и обычные
ноды, которые находятся под управлением мастер-ноды.
Для создания кластера необходим создать или использовать созданный публичный ключ.


Объект "кластер kubernetes"
---------------------------

.. autoclass:: esu.Kubernetes


Примеры использования
---------------------

Создать кластер kubernetes:

.. code-block:: python

  from esu import Vdc, Kubernetes, PublicKey
  vdc = Vdc.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  key = PublicKey.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  storage_profile = vdc.get_storage_profiles()[0]  # Первый доступный профиль хранения
  k8s_template = next(v for v in vdc.get_k8s_templates() if 'Kubernetes 1.22.1' in v.name)  # Шаблон кластера
  cluster = Kubernetes(name="MyK8S", vdc=vdc, node_cpu=2, node_ram=2,
                       node_disk_size=10, node_storage_profile=storage_profile,
                       nodes_count=2, template=k8s_template, user_public_key=key)