from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(slots=True)  # меньше памяти, быстрее доступ
class Node:
    id: int
    name: str
    url: str | None
    level: int
    query_param: str | None = None
    parent: Node | None = None
    children: list[Node] = field(default_factory=list)

    categories_url: str | None = None
    categories: list[str] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return not self.children

    def breadcrumb(self) -> list[str]:
        path = []
        node = self
        while node:
            path.append(node.name)
            node = node.parent
        return list(reversed(path))  # от корня до текущего узла
