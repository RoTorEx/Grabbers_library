from bs4 import BeautifulSoup
import sys
import json
import requests
import time
import datetime
import aiohttp
import asyncio


def default_config():
    '''Creating config.'''
    return dict(
        # Grabber settings
        headers={},
        pages='',

        # Async settings
        grab_sleep=0.15,
        grab_limit=50
    )


class Grabber():
    '''Grab info from site.'''

    __slots__ = ('url', 'config', 'finished_pages', 'data')

    def __init__(self, initial_values, *args, **kwargs):
        self.config = default_config()

        self.url = initial_values['url']
        self.config['headers'] = self.common_headers()
        self.config['pages'] = initial_values['pages']
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

            page_items = soup.find("div", class_="grid__catalog")

            for item in page_items:
                try:
                    brand = item.find("div", class_="product-card__brand-name").text.strip()
                except:
                    brand = "No brand."

                try:
                    product = item.find("div", class_="product-card__product-name").text.strip()
                except:
                    product = "No product."

                try:
                    old_price = item.find("span", class_="product-card__price_old").text.strip(" Рр.") + " p."
                except:
                    old_price = "No old price."

                try:
                    new_price = item.find("span", class_="product-card__price_new").text.strip(" Рр.") + " p."
                except:
                    new_price = "No new price."

                try:
                    sizes = []
                    for size in item.find("div", class_="product-card__sizes"):
                        sizes.append(size.text.strip())
                except:
                    sizes = "No available sizes."

                try:
                    link = "https://www.lamoda.by" + item.find("a").get('href')
                except:
                    link = "No link."

                self.data.append(
                    {
                        "brand": brand,
                        "product": product,
                        "old_price": old_price,
                        "new_price": new_price,
                        "sizes": sizes,
                        "link": link,
                    }
                )

            self.finished_pages += 1
            await asyncio.sleep(self.config['grab_sleep'])

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

    def get_pages_count(self, url):
        '''Makes a request to the site to find the number of pages.'''

        url += "?page=1&json=1"
        response = requests.get(url=url, headers=self.config['headers'])
        jsoned_html = json.loads(response.content)

        return int(jsoned_html['payload']['pagination']['pages'])

    def run_grabber(self, url):
        '''Create loop for grabber and start it.'''

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.gather_data(url, self.config['headers'], self.config['pages']))

    def write_data(self, url):
        '''Write collected data to .json file and initial config to .txt file.'''

        cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

        with open(f"data/{cur_time}_items.json", "w") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

        with open(f"data/{cur_time}_config.txt", "w") as file:
            x = ' | '
            link = f"Link{x.rjust(6)}{url}"
            pages = f"Pages{x.rjust(5)}{self.config['pages']}"
            print(link, pages, sep='\n', file=file)

    def end(self, start_time):
        '''Print spent time to console.'''

        finish_time = time.time() - start_time
        spent_time = time.strftime("%M:%S (min:sec)", time.gmtime(finish_time))
        print(f"\nElapsed time to script's work: {spent_time}.")

    def start(self):
        '''Method starts grabber.'''

        start_time = time.time()

        if self.config['pages'] is None:
            self.config['pages'] = self.get_pages_count(self.url)

        elif self.config['pages'].isdigit():
            self.config['pages'] = int(self.config['pages'])

        elif not self.config['pages'].isdigit():
            raise ValueError("Value must be integer or 'all'!")

        self.run_grabber(self.url)
        self.write_data(self.url)
        self.end(start_time)
