from bs4 import BeautifulSoup
import sys
import json
import requests
import time
import datetime
import aiohttp
import asyncio


start_time = time.time()
products_data = []
finished = 0


def get_pages_count():
    '''Method makes a request to the site to find the number of pages.'''

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36",  # noqa: E501
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    url = "https://www.lamoda.by/c/4152/default-men/?page=1&json=1"

    response = requests.get(headers=headers, url=url)

    jsoned_html = json.loads(response.content)

    pages_count = jsoned_html['payload']['pagination']['pages']

    # with open("json_page.json", "w") as file:
    #     json.dump(jsoned_html, file, indent=4, ensure_ascii=False)

    return pages_count


async def get_page_data(session, page, pages_count):
    '''Asynchronous function which collect data from the submitted page.'''

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36",  # noqa: E501
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    url = f"https://www.lamoda.by/c/4152/default-men/?page={page}"

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

            products_data.append(
                {
                    "brand": brand,
                    "product": product,
                    "old_price": old_price,
                    "new_price": new_price,
                    "sizes": sizes,
                    "link": link,
                }
            )

        global finished
        finished += 1
        await asyncio.sleep(.1)

        sys.stdout.write(u"\u001b[1000D")
        sys.stdout.write(f"Pages parsered: ==< {finished}/{pages_count} >==")
        sys.stdout.flush()


async def gather_data(pages_count):
    '''Asynchronous function which creates tasks-functions.'''
    connector = aiohttp.TCPConnector(verify_ssl=False, limit=10)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page, pages_count))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    pages_count = get_pages_count()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_data(pages_count))

    with open(f"lamoda_items_{cur_time}.json", "w") as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)

    finish_time = time.time() - start_time
    spent_time = time.strftime("%M:%S (min:sec)", time.gmtime(finish_time))

    print(f"\nElapsed time to script's work: {spent_time}.")


if __name__ == "__main__":
    main()
