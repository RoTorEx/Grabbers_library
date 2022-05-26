import datetime
import time
import json


class DataOutput():
    def write_data(url, data, pages):
        '''Write collected data to .json file and initial config to .txt file.'''

        cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

        with open(f"data/{cur_time}_items.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        with open(f"data/{cur_time}_config.txt", "w") as file:
            x = ' | '
            link = f"Link{x.rjust(6)}{url}"
            pages = f"Pages{x.rjust(5)}{pages}"
            print(link, pages, sep='\n', file=file)

    def end(start_time):
        '''Print spent time to console.'''

        finish_time = time.time() - start_time
        spent_time = time.strftime("%M:%S (min:sec)", time.gmtime(finish_time))
        print(f"\nElapsed time to script's work: {spent_time}.")
