import asyncio

import httpx

from parser import WildberriesParser
from wildberries_client import WildberriesClient


async def shoes_use_case():
    http_client = httpx.AsyncClient(timeout=10.0)
    wildberries_client = WildberriesClient(http_client)

    main_page_json = await wildberries_client.get_main_wildberries_page()
    root_nodes = WildberriesParser.process_page_json(main_page_json)
    print(root_nodes)





if __name__ == '__main__':
    asyncio.run(shoes_use_case())
