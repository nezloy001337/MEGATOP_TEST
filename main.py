import asyncio
from datetime import datetime

import httpx

from parser import WildberriesParser
from wildberries_client import WildberriesClient


async def categories_use_case():
    http_client = httpx.AsyncClient(timeout=10.0)
    wildberries_client = WildberriesClient(http_client)

    # получаем json с категориями
    main_page_json = await wildberries_client.get_main_wildberries_page()

    # строим дерево из категорий
    root_nodes = WildberriesParser.process_page_json(main_page_json)

    # достаем листья - последняя вложенность
    leafs = WildberriesParser.get_leafs(root_nodes)

    # создаем ссылки на json с категориями для листьев
    WildberriesParser.set_categories_url(leafs)

    time_before = datetime.now()
    # получаем вариации предметов для листьев
    await wildberries_client.get_categories_for_leafs(leafs)

    time_after = datetime.now()
    spent = time_after - time_before
    print(spent)





if __name__ == "__main__":
    asyncio.run(categories_use_case())
