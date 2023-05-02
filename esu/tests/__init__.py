import json
import os

import responses

from esu.base import BaseAPI


def load_fixtures(func):
    def wrapper(*args, **kwargs):
        BaseAPI.endpoint_url = 'https://api.example.com'

        filename = os.path.join(os.path.dirname(__file__), 'fixtures.json')

        with responses.RequestsMock(
                assert_all_requests_are_fired=False) as rsps:
            with open(filename, 'r', encoding='utf-8') as fh:
                cases = json.loads(fh.read())

            for data in cases:
                has_querystring = data['method'] in ('GET', 'DELETE')
                method = getattr(responses, data['method'])
                params = {
                    'method': method,
                    'url': data['url'],
                    'json': data['response'],
                    'status': data['status'],
                    'content_type': 'application/json',
                    'match_querystring': has_querystring
                }

                if not has_querystring:
                    # Check request body
                    params['match'] = \
                        [responses.json_params_matcher(data['request'])]

                rsps.add(**params)

            result = func(rsps, *args, **kwargs)
            return result

    return wrapper
