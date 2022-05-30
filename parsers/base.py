from typing import Optional, List
import dataclasses
import abc

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys
import json
import time
import datetime
import aiohttp
import asyncio


@dataclasses.dataclass
class Entry:
    name: str
    price: str
    link: Optional[str]
    common: dict


class BaseParser(abc.ABC):

    BASE_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36",  # noqa: E501
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }
    BASE_URL = NotImplemented
    COLLECT_DATA = []
    FINISH_PAGES = 0
    TIME = {"start": 0, "end": 0}

    @abc.abstractmethod
    def parse(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def clean(self, *args, **kwargs) -> List[Entry]:

        cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

        with open(f"data/{cur_time}_items.json", "w") as file:
            json.dump(self.COLLECT_DATA, file, indent=4, ensure_ascii=False)

        self.TIME['end'] = time.time()
        spent_time = (f"{self.TIME['end'] - self.TIME['start']:.4}")
        print(f"\nElapsed time to script's work: {spent_time} seconds.")

    @abc.abstractmethod
    def run(self, pages_count, *args, **kwargs):
        self.TIME['start'] = time.time()

        async def gather_data(self, url, headers, pages_count):
            '''Asynchronous function which creates tasks-functions.'''

            connector = aiohttp.TCPConnector(verify_ssl=False, limit=50)

            async with aiohttp.ClientSession(connector=connector) as session:
                tasks = []

                for page in range(1, pages_count + 1):
                    task = asyncio.create_task(self.parse(session, page, pages_count, headers, url))
                    tasks.append(task)

                await asyncio.gather(*tasks)

                self.clean()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(gather_data(self, self.BASE_URL, self.BASE_HEADERS, pages_count))
