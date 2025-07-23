import logging
from typing import Optional
from urllib.parse import urlencode, quote_plus

from models import Node

logger = logging.getLogger(__name__)


class WildberriesParser:
    @staticmethod
    def process_page_json(main_page_json):
        return [WildberriesParser._build_tree(node) for node in main_page_json[3:-2]]

    @staticmethod
    def _build_tree(data: dict, level: int = 0, parent: Node | None = None) -> Node:
        node = Node(
            id=data["id"],
            name=data["name"],
            url=data.get("url"),
            level=level,
            parent=parent,
        )

        for child_data in data.get("childs", []):
            child_node = WildberriesParser._build_tree(child_data, level + 1, node)
            node.children.append(child_node)

        return node

    @staticmethod
    def get_leafs(root_nodes: list[Node]):
        leafs = []
        for node in root_nodes:
            leafs.extend(WildberriesParser._get_leaf_nodes(node))

        return leafs

    @staticmethod
    def set_categories_url(leafs: list[Node]):
        for leaf in leafs:
            leaf.categories_url = WildberriesParser._build_leaf_filter_url(leaf)

    @staticmethod
    def _get_leaf_nodes(root: Node) -> list[Node]:
        leaves = []

        def walk(node: Node):
            if not node.children:
                leaves.append(node)
            for child in node.children:
                walk(child)

        walk(root)
        return leaves

    @staticmethod
    def _build_leaf_filter_url(node: Node) -> Optional[str]:
        if node.children:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return None  # не leaf, не строим ссылку

        base_url = "https://search.wb.ru/exactmatch/ru/common/v14/search"

        query_params = {
            "ab_testid": "pfact_gr_2",
            "appType": "1",
            "curr": "rub",
            "dest": "-1255987",
            "hide_dtype": "13;14",
            "lang": "ru",
            "query": f"menu_redirect_subject_v2_{node.id} {node.name}",
            "resultset": "filters",
            "spp": "30",
            "suppressSpellcheck": "false",
        }

        return f"{base_url}?{urlencode(query_params, quote_via=quote_plus)}"
