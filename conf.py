import json
import requests


class Config():
    def default_config():
        '''Creating config.'''
        return dict(
            # Grabber settings
            headers={},

            # Async settings
            grab_sleep=0.15,
            grab_limit=50
        )

    def test_connection(url, headers):
        response = requests.get(url=url, headers=headers)

        if response.status_code not in [200, ]:
            raise ConnectionError("Unable to connect to server")

    def get_pages_count(url, headers):
        '''Makes a request to the site to find the number of pages.'''

        url += "?page=1&json=1"
        response = requests.get(url=url, headers=headers)
        jsoned_html = json.loads(response.content)

        return int(jsoned_html['payload']['pagination']['pages'])
