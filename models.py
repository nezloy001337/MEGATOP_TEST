from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Node:
    id: int
    name: str
    url: Optional[str]
    level: int
    parent: Optional["Node"] = None
    children: List["Node"] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return not self.children

    def breadcrumb(self) -> List[str]:
        path = []
        node = self
        while node:
            path.append(node.name)
            node = node.parent
        return list(reversed(path))  # от корня до текущего узла

