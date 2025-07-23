import logging

logger = logging.getLogger(__name__)


def find_categories_key(all_data: list[dict]):
    for data in all_data:
        if data.get("name") == "Категория":
            return data["items"]

    raise Exception()

