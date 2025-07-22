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

    @staticmethod
    def get_leaf_nodes(root: Node) -> list[Node]:
        leaves = []

        def walk(node: Node):
            if not node.children:
                leaves.append(node)
            for child in node.children:
                walk(child)

        walk(root)
        return leaves
