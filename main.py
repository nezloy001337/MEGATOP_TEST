import asyncio
from datetime import datetime

import httpx

from excel import save_trees_to_excel
from parser import WildberriesParser
from wildberries_client import WildberriesClient


async def categories_use_case():
    time_before = datetime.now()
    http_client = httpx.AsyncClient(timeout=7.0)
    wildberries_client = WildberriesClient(http_client)

    # получаем json с категориями
    main_page_json = await wildberries_client.get_main_wildberries_page()

    # строим дерево из категорий
    root_nodes = WildberriesParser.process_page_json(main_page_json)

    # достаем листья - последняя вложенность категорий
    leafs = WildberriesParser.get_leafs(root_nodes)

    # создаем ссылки на json с категориями для листьев
    WildberriesParser.set_categories_url(leafs)

    # получаем вариации предметов для листьев
    await wildberries_client.get_categories_for_leafs(leafs)

    # cохраняем в excel
    save_trees_to_excel(root_nodes)

    time_after = datetime.now()
    spent = time_after - time_before
    print(spent)



if __name__ == "__main__":
    asyncio.run(categories_use_case())
