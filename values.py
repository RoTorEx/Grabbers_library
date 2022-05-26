def input_initial_values():
    '''Input here initial values to start site grabber.'''

    url = input('Enter URL site: ')
    # url = "https://www.lamoda.by/c/4152/default-men/"

    search_block = (input("Enter the searching tag: "), input("Enter the class_name to searching tag: ")),
    # search_block = ("div", "product-card")

    while True:
        search_fields = {}
        key_input = input("Enter tag which need to grab: ").strip()
        value_input = input("Enter class-name of tag: ").strip()

        if not key_input or not value_input:
            break

        if key_input not in search_fields:
            search_fields.setdefault(key_input, [value_input, ])
            continue

        elif key_input in search_fields:
            search_fields[key_input].append(value_input)
            continue
    # search_fields = {"div": ["product-card__brand-name", "product-card__product-name", "product-card__sizes"],
    #                  "span": ["product-card__price_old", "product-card__price_new"],
    #                  "a": ["href"]}

    while True:
        pages_input = input("Enter the page number which need to grab (skip - 1, 0 - all): ")
        if pages_input == '':
            pages = 1
            break

        elif pages_input.isdigit():
            pages = int(pages_input)
            break

        elif not pages_input.isdigit():
            continue
    # pages = 1

    keys = ('url', 'block', 'fields', 'pages', )
    initial_values = dict(zip(keys, (url, search_block, search_fields, pages)))

    return initial_values
