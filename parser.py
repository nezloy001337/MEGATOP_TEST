import logging

from models import Node

logger = logging.getLogger(__name__)


class WildberriesParser:
    @staticmethod
    def process_page_json(main_page_json):
        return [WildberriesParser._build_tree(node) for node in main_page_json]

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
