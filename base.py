from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys
import time
import aiohttp
import asyncio

from conf import Config
from out import DataOutput


class Grabber():
    '''Site grabber.'''

    __slots__ = ('url', 'block', 'fields', 'pages', 'config', 'finished_pages', 'data')

    def __init__(self, initial_values, *args, **kwargs):
        self.config = Config.default_config()

        self.url = initial_values['url']
        self.block = {'tag': initial_values['block'][0], 'class': initial_values['block'][1]}
        self.fields = initial_values['fields']
        self.pages = initial_values['pages']
        self.config['headers'] = self.common_headers()

        self.finished_pages = 0
        self.data = []

    @classmethod
    def common_headers(cls):
        '''Build headers which sends typical browser.'''

        return {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36",  # noqa: E501
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        }

    async def get_page_data(self, session, page, pages_count, headers, url):
        '''Asynchronous function which collect data from the submitted page.'''

        url += f"?page={page}"

        async with session.get(url=url, headers=headers) as response:
            response_text = await response.text()

            soup = BeautifulSoup(response_text, "lxml")

            items = soup.find_all(self.block['tag'], class_=self.block['class'])

            for item in items:
                item_dict = {}

                for key, values in self.fields.items():
                    for value in values:

                        if key == 'a' and value == 'href':
                            try:
                                netloc = urlparse(self.url)
                                item_dict['link'] = f"{netloc[0]}://{netloc[1]}" + item.find("a").get('href')

                            except:
                                item_dict['link'] = "None"

                            continue

                        try:
                            item_list = []
                            for char in item.find(key, class_=value):
                                item_list.append(char.text.strip())

                            current_value = ' '.join(item_list)
                            item_dict[value] = current_value

                        except:
                            item_dict[value] = "None"

                else:
                    self.data.append(item_dict)

            await asyncio.sleep(self.config['grab_sleep'])

            self.finished_pages += 1

            sys.stdout.write(u"\u001b[1000D")
            sys.stdout.write(f"Pages grabbed: ==< {self.finished_pages}/{pages_count} >==")
            sys.stdout.flush()

    async def gather_data(self, url, headers, pages_count):
        '''Asynchronous function which creates tasks-functions.'''

        connector = aiohttp.TCPConnector(verify_ssl=False, limit=self.config['grab_limit'])

        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []

            for page in range(1, pages_count + 1):
                task = asyncio.create_task(self.get_page_data(session, page, pages_count, headers, url))
                tasks.append(task)

            await asyncio.gather(*tasks)

    def run_grabber(self, url):
        '''Create loop for grabber and start it.'''

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.gather_data(url, self.config['headers'], self.pages))

    def start(self):
        '''Method starts grabber.'''

        Config.test_connection(self.url, self.config['headers'])

        start_time = time.time()

        if self.pages == 0:
            self.pages = Config.get_pages_count(self.url, self.config['headers'])

        self.run_grabber(self.url)

        DataOutput.write_data(self.url, self.data, self.pages)
        DataOutput.end(start_time)
