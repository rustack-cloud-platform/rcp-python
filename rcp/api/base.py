import os
import re
import sys
from time import sleep, time

import requests

from .consts import DEFAULT_TIMEOUT


class BaseEx(Exception):
    pass


class NotFoundEx(BaseEx):
    pass


class TaskTimeoutEx(BaseEx):
    pass


class ObjectAlreadyHasId(BaseEx):
    pass


class ObjectHasNoId(BaseEx):
    pass


class PortAlreadyConnected(BaseEx):
    pass


class TaskFailed(BaseEx):
    pass


class Field:
    def __init__(self, class_name=None, *, allow_none=False):
        self._class_name = class_name
        self._allow_none = allow_none

    @property
    def cls(self):
        return resolve(self._class_name)


class FieldList(Field):
    pass


def resolve(cls):
    if isinstance(cls, str):
        cls2 = []
        for item in cls.split('.'):
            # CamelCase to snake_case:
            cls2.append(re.sub(r'(?<!^)(?=[A-Z])', '_', item).lower())
        cls2 = '.'.join(cls2)  # rcp.StorageProfile -> rcp.storage_profile

        cls = getattr(sys.modules[cls2], cls.split('.')[-1])

    return cls


class RCPConfig:
    endpoint_url = ''
    token = None
    test_mode = False

    @classmethod
    def load(cls, endpoint_url, token, test_mode):
        cls.endpoint_url = endpoint_url
        cls.token = token
        cls.test_mode = test_mode


class BaseAPI:
    token = None
    endpoint_url = ''
    test_mode = False

    def __new__(cls, *args, token: str = None, endpoint_url: str = '',
                test_mode: bool = False, **kwargs):
        rules = {}
        for k in cls.Meta.__dict__:
            if k.startswith('_'):
                continue
            rules[k] = cls.Meta.__dict__[k]

        instance = super().__new__(cls)
        instance._rules = rules

        for k in rules:
            setattr(instance, k, None)

        instance.token = (token or RCPConfig.token or
                          os.environ.get('RCP_API_TOKEN', cls.token))
        instance.endpoint_url = (endpoint_url or
                                 RCPConfig.endpoint_url or os.environ.get(
                                     'RCP_API_URL', cls.endpoint_url))
        instance.test_mode = (test_mode or RCPConfig.test_mode or
                              os.environ.get('RCP_TEST_MODE', cls.token))
        instance.kwargs = kwargs
        instance._fill()

        return instance

    def __repr__(self):
        return '{} ({})'.format(self.__class__, self.id)

    def _call(self, http_method, resource, wait=True, timeout='default',
              **kwargs):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json',
            'Accept-Language': 'ru-ru'
        }

        url = '{}/{}'.format(self.endpoint_url, resource)
        request_params = {'url': url, 'headers': headers, 'timeout': 30}
        http_method = http_method.lower()

        request_params['params' if http_method == 'get' else 'json'] = kwargs
        method_ = getattr(requests, http_method)
        resp = method_(**request_params)

        answer = None
        if self.test_mode and 'job' not in resource:
            self._test_mode(resp)
        elif resp.status_code == 404:
            raise NotFoundEx('Resource not found')
        else:
            resp.raise_for_status()

        if resp.status_code not in (202, 204):
            if 'config' in resource:
                answer = resp.text
            else:
                answer = resp.json()

        for task_id in resp.headers.get('X-Esu-Tasks', '').split(','):
            task_id = task_id.strip()
            if not task_id:
                continue
            self._wait_job(task_id, wait, timeout)

        return answer

    def _wait_job(self, job_id, wait, timeout):
        if timeout == 'default':
            timeout = DEFAULT_TIMEOUT
        start_time = time()

        while wait:
            if timeout is not None:
                if time() - start_time > timeout:
                    raise TaskTimeoutEx("Time for waiting a task is expired")

                try:
                    job = self._call('GET', 'v1/job/{}'.format(job_id))
                    if job['status'] == 'error':
                        raise TaskFailed("Task is failed")
                    sleep(1)
                except NotFoundEx:
                    break

    def get_list(self, resource, cls, with_pages=True, **kwargs):
        result = []

        if not with_pages:
            answer = self._call('GET', resource, **kwargs)
            for item in answer:
                instance = resolve(cls)(token=self.token, **item)
                result.append(instance)
            return result

        page = 1
        while True:
            kwargs['page'] = page
            try:
                answer = self._call('GET', resource, **kwargs)
            except NotFoundEx:
                break

            for item in answer['items']:
                instance = resolve(cls)(token=self.token, **item)
                result.append(instance)
            if len(result) == answer['total']:
                break
            page += 1

        return result

    def _fill(self):
        for k, v in self.kwargs.items():
            if k not in self._rules:
                continue

            fld = self._rules[k]
            v_new = None

            if fld._allow_none and v is None:
                pass  # v_new is None
            elif isinstance(fld, FieldList):
                v_new = []
                for obj in v:
                    if v is None:
                        raise ValueError

                    if isinstance(obj, BaseAPI):
                        v_new.append(obj)
                    elif isinstance(obj, str):  # ID case
                        v_new.append(fld.cls.retrieve(obj, token=self.token))
                    else:  # dict
                        v_new.append(fld.cls(**obj))
            elif isinstance(fld, Field):
                if isinstance(v, BaseAPI) or fld.cls is None:
                    v_new = v
                elif isinstance(v, str):  # ID case
                    v_new = fld.cls.retrieve(v)
                else:  # dict
                    v_new = fld.cls(**v)

            setattr(self, k, v_new)

    def _get_object(self, resource, id):
        self.kwargs = self._call('GET', '{}/{}'.format(resource, id))
        self._fill()

    def _commit_object(self, resource, wait=True, timeout='default', **kwargs):
        if self.id is None:
            self.kwargs = self._call('POST', resource, wait, timeout, **kwargs)
        else:
            self.kwargs = self._call('PUT', '{}/{}'.format(resource, self.id),
                                     wait, timeout, **kwargs)
        self._fill()

    def _destroy_object(self, resource, id, wait=True, timeout='default'):
        self._call('DELETE', '{}/{}'.format(resource, id), wait, timeout)
        self.id = None

    def _patch_object(self, resource, id, wait=True, timeout='default'):
        self._call('PATCH', '{}/{}'.format(resource, id), wait, timeout)
        self._fill()

    def _test_mode(self, resp):
        setattr(self, 'status_code', resp.status_code)
        if resp.status_code not in (202, 204):
            setattr(self, 'body', resp.json())
