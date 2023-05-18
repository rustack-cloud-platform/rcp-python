Image
=======

Образ - образ сервера или iso образ какой либо программы или ОС.
Создать образ можно из уже созданного сервера, например для последующего
создании копии этого сервера, путем создания сервера из образа.
Также в сегменте VMware можно загрузить образ в систему, для последующего
создания сервера из образа или для монтирования образа к серверу (iso)


Объект "образ"
---------------

.. autoclass:: esu.Image


Примеры использования
---------------------

Создать образ из созданного сервера:

.. code-block:: python

  from esu import Vm, Image, Vdc

  vm = Vm.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vdc = Vdc.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  image = Image(vdc=vdc, name='NewImage')
  image.create_from_vm(vm=vm)


Загрузить образ:

.. code-block:: python

  import requests
  from esu import Image, Vdc

  vdc = Vdc.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  image = Image(vdc=vdc, name='NewImage')
  image.create_for_upload() # Создание объекта образа для последующей загрузки файлов
  url = image.get_upload_link() # Получение ссылки для загрузки файлов

  headers = {
            'Accept': '* / *',
            'Accept-Encoding': 'gzip, deflate, br',
            'Authorization': "bearer " + str(BaseAPI.token),
            'Connection': 'keep-alive',
            'Content-Type': 'application/octet-stream',
            'Accept-Language': 'ru-ru'
        }
  file = {'file': open('test.iso', 'rb')}
  up_response = requests.put(url=str(url), headers=headers, files=file) # Загрузка файла

  image.commit_upload() # Подтверждение окончания загрузки файлов образа


Создание сервера из образа:

.. code-block:: python

  from esu import Image

  image = Image.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  vm = image.deploy_vm_from_image()

