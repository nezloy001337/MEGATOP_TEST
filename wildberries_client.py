import asyncio
import logging
import random
from functools import wraps

from aiolimiter import AsyncLimiter
from httpx import AsyncClient, HTTPError

from models import Node

logger = logging.getLogger(__name__)


def retry_async(
    retries=4,
    base_delay=4,
    max_delay=30,
    jitter=2,
    exceptions=(ValueError, HTTPError),  # connection timeout and ext.
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == retries:
                        raise Exception("max retries exceeded")
                    raw_delay = min(max_delay, base_delay * (attempt + 1))
                    sleep_time = max(0.0, raw_delay + random.uniform(-jitter, jitter))
                    logger.info(
                        "Error occurred while working with api. Retrying after %s seconds. Error: %s",
                        sleep_time,
                        e,
                    )
                    await asyncio.sleep(sleep_time)

        return wrapper

    return decorator


class WildberriesClient:
    def __init__(
        self,
        httpx_client: AsyncClient,
    ):
        self.httpx_client = httpx_client
        self.limiter = AsyncLimiter(max_rate=70, time_period=1)

    async def _get_request(self, url: str):
        async with self.limiter:
            response = await self.httpx_client.get(url)
        return response

    @retry_async(retries=3)
    async def get_main_wildberries_page(self):
        # все данные по категориям, которые приходят на главную страницу, берутся здесь
        url = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"
        response = await self._get_request(url=url)

        if response.status_code != 200:
            raise Exception(
                "Status code %s is not expected. Response: %s"
                % (response.status_code, response.text)
            )

        return response.json()

    @retry_async(retries=3)
    async def _get_categories_json(self, url):
        response = await self._get_request(url=url)

        if response.status_code != 200:
            raise ValueError(
                f"Status code {response.status_code} is not expected. Retrying..."
            )

        return response.json()

    async def _leaf_task(self, leaf: Node):
        categories_json = await self._get_categories_json(leaf.categories_url)
        categories = categories_json["data"]["filters"][0]["items"]
        print(categories)
        leaf.categories = categories

    async def get_categories_for_leafs(self, leafs: list[Node]):
        leaf_tasks = [self._leaf_task(leaf) for leaf in leafs]
        results = await asyncio.gather(*leaf_tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error("не получилось получить данные для %s", result)
