from bs4 import BeautifulSoup
import sys
import asyncio

from parsers.base import BaseParser


class LamodaParser(BaseParser):

    BASE_URL = "https://www.lamoda.by"

    def parse(self, session, page, pages_count, headers, url, *args, **kwargs):
        super().parse()

        async def get_page_data(self, session, page, pages_count, headers, url):
            '''Asynchronous function which collect data from the submitted page.'''

            url += f"/c/4152/default-men/?page={page}"

            async with session.get(url=url, headers=headers) as response:
                response_text = await response.text()

                soup = BeautifulSoup(response_text, "lxml")

                page_items = soup.find("div", class_="grid__catalog")

                if page_items:
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
                            sizes = ' | '.join(sizes).strip('|')

                        except:
                            sizes = "No available sizes."

                        try:
                            link = "https://www.lamoda.by" + item.find("a").get('href')
                        except:
                            link = "No link."

                        name = f"{brand} - {product}"
                        price = f"New: {new_price} | Old: {old_price}"
                        link = link
                        common = {"sizes": sizes}

                        super().COLLECT_DATA.append(
                            {
                                "name": name,
                                "price": price,
                                "common": common,
                                "link": link,
                            }
                        )

                await asyncio.sleep(0.2)

                self.FINISH_PAGES += 1

                sys.stdout.write(u"\u001b[1000D")
                sys.stdout.write(f"Pages grabbed: ==< {self.FINISH_PAGES}/{pages_count} >==")
                sys.stdout.flush()

        return get_page_data(self, session, page, pages_count, headers, url)

    def clean(self, *args, **kwargs):
        super().clean()

    def run(self, *args, **kwargs):
        super().run(pages_count=args[1])
