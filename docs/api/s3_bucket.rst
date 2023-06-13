S3Bucket
================

Бакет хранилища S3. Файловая корзина - элемент S3 хранилища, который
использует для хранения файлов и папок в хранилище S3.


Объект "бакет хранилища S3"
---------------------------

.. autoclass:: esu.S3Bucket


Примеры использования
---------------------

Создать бакет объектного хранилища S3:

.. code-block:: python

  from esu import S3, S3bucket

  s3 = S3.get_object('d5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9')
  s3bucket = S3Bucket(name="MyS3bucket", s3=s3)
  s3bucket.create()

