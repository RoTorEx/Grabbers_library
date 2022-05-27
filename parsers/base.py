from typing import Optional, List
import dataclasses
import abc


@dataclasses.dataclass
class Entry:
    price: int
    name: str
    description: Optional[str]


class BaseParser(abc.ABC):

    BASE_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Mobile Safari/537.36",  # noqa: E501
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }
    BASE_URL = NotImplemented

    @abc.abstractmethod
    def parse(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def clean(self, *args, **kwargs) -> List[Entry]:
        pass

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        pass
