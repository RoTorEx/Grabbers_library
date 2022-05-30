from pathlib import Path
import os

from parsers.lamoda import LamodaParser


def main():
    site = ParserRunner()
    site.run(site.site_parser)


class ParserRunner:

    __slots__ = ("site_name", "site_parser", "pages")

    PARSERS = {
        "lamoda": LamodaParser()
    }

    def __init__(self):
        parsers_list = (map(lambda file: file.strip('.py'),
                            filter(lambda file: file not in ['__init__.py', '__pycache__', 'base.py'],
                                   os.listdir(f"{Path.cwd()}/parsers"))))

        self.site_name = input("Enter site name, please: ").strip().split('.')[0]
        self.pages = int(input("Enter count of pages which you like to parse: "))

        if self.site_name in parsers_list:
            self.site_parser = self.PARSERS[self.site_name]

            # self.run(self.site_parser)  # Creating an instance of a class

        else:
            raise AttributeError("There is no ready parser for this site yet. Or check the site name and try again.")

    def run(self, parser):
        parser.run(self, self.pages)  # Run method of parser-class instance


if __name__ == "__main__":
    main()
