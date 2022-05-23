from bs4 import BeautifulSoup
import sys
import json
import requests
import time
import datetime


start_time = time.time()


def get_data():

    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }

    url = "https://www.lamoda.by/c/4152/default-men/"

    items_data = []

    print("Parsering in process...")

    for page in range(1, 168):
        url += f"?page={page}"

        response = requests.get(headers=headers, url=url)

        soup = BeautifulSoup(response.text, "lxml")

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

            items_data.append(
                {
                    "brand": brand,
                    "product": product,
                    "old_price": old_price,
                    "new_price": new_price,
                    "sizes": sizes,
                    "link": link,
                }
            )

        sys.stdout.write(u"\u001b[1000D")
        sys.stdout.write(f"Pages parsered: ==< {page} >==")
        sys.stdout.flush()
        time.sleep(.5)

    with open(f"lamoda_items_{cur_time}.json", "w") as file:
        json.dump(items_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"\nElapsed time to script's work: {finish_time} seconds.")


if __name__ == "__main__":
    main()
