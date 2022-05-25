from base import Grabber


def main():
    keys = ('url', 'pages', )

    input_data = map(lambda x: None if x == '' else x, (
        "https://www.lamoda.by/c/4152/default-men/",
        # input('Enter URL site: '),
        input('Enter count of pages or skip to grab all: ')
    ))

    initial_values = dict(zip(keys, input_data))

    site = Grabber(initial_values)
    site.start()


if __name__ == "__main__":
    main()
