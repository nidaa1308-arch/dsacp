from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable
import math

@dataclass
class KDNode:
    point: tuple[float, float]
    payload: Any
    axis: int
    left: "KDNode | None" = None
    right: "KDNode | None" = None

class KDTree:
    """2-D KD-Tree with balanced median construction and nearest-neighbour query."""
    def __init__(self, items: Iterable[tuple[tuple[float, float], Any]] = ()):
        data = list(items)
        self.size = len(data)
        self.root = self._build(data, 0)

    def _build(self, items, depth):
        if not items:
            return None
        axis = depth % 2
        items.sort(key=lambda item: item[0][axis])
        mid = len(items) // 2
        point, payload = items[mid]
        return KDNode(
            point=point, payload=payload, axis=axis,
            left=self._build(items[:mid], depth + 1),
            right=self._build(items[mid + 1:], depth + 1),
        )

    def nearest(self, target: tuple[float, float]):
        if self.root is None:
            return None
        best_node, best_d2, visited = None, float("inf"), 0

        def visit(node):
            nonlocal best_node, best_d2, visited
            if node is None:
                return
            visited += 1
            dx = node.point[0] - target[0]
            dy = node.point[1] - target[1]
            d2 = dx * dx + dy * dy
            if d2 < best_d2:
                best_node, best_d2 = node, d2

            axis = node.axis
            delta = target[axis] - node.point[axis]
            near, far = (node.left, node.right) if delta < 0 else (node.right, node.left)
            visit(near)
            if delta * delta < best_d2:
                visit(far)

        visit(self.root)
        return {
            "point": best_node.point,
            "payload": best_node.payload,
            "distance": math.sqrt(best_d2),
            "nodes_visited": visited,
            "tree_size": self.size,
        }
