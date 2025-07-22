from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Node:
    id: int
    name: str
    url: str | None
    level: int
    parent: Node | None = None
    children: list[Node] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return not self.children

    def breadcrumb(self) -> list[str]:
        path = []
        node = self
        while node:
            path.append(node.name)
            node = node.parent
        return list(reversed(path))  # от корня до текущего узла

