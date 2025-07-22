import asyncio
import logging
import random
from functools import wraps

from aiolimiter import AsyncLimiter
from httpx import AsyncClient, HTTPError

logger = logging.getLogger(__name__)


def retry_async(
    retries=4,
    base_delay=4,
    max_delay=30,
    jitter=2,
    exceptions=HTTPError,  # connection timeout and ext.
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
        self.limiter = AsyncLimiter(max_rate=1, time_period=0.35)

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
