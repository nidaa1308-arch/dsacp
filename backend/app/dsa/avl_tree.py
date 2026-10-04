from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class AVLNode:
    key: float
    value: Any
    height: int = 1
    left: "AVLNode | None" = None
    right: "AVLNode | None" = None

class AVLTree:
    """AVL balanced BST used as the sweep-line active status structure."""
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def _h(node): return node.height if node else 0
    def _update(self, node): node.height = 1 + max(self._h(node.left), self._h(node.right))
    def _balance(self, node): return self._h(node.left) - self._h(node.right)

    def _rotate_right(self, y):
        x, t2 = y.left, y.left.right
        x.right, y.left = y, t2
        self._update(y); self._update(x)
        return x

    def _rotate_left(self, x):
        y, t2 = x.right, x.right.left
        y.left, x.right = x, t2
        self._update(x); self._update(y)
        return y

    def insert(self, key: float, value: Any):
        inserted = [False]
        def rec(node):
            if node is None:
                inserted[0] = True
                return AVLNode(key, value)
            if (key, id(value)) < (node.key, id(node.value)):
                node.left = rec(node.left)
            else:
                node.right = rec(node.right)
            self._update(node)
            b = self._balance(node)
            if b > 1:
                if key < node.left.key:
                    return self._rotate_right(node)
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
            if b < -1:
                if key >= node.right.key:
                    return self._rotate_left(node)
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
            return node
        self.root = rec(self.root)
        if inserted[0]: self.size += 1

    def inorder(self):
        out = []
        def walk(n):
            if not n: return
            walk(n.left); out.append((n.key, n.value)); walk(n.right)
        walk(self.root)
        return out

    def neighbours_by_value(self, value: Any):
        ordered = self.inorder()
        for i, (_, v) in enumerate(ordered):
            if v is value:
                prev_v = ordered[i - 1][1] if i > 0 else None
                next_v = ordered[i + 1][1] if i + 1 < len(ordered) else None
                return prev_v, next_v
        return None, None

    def rebuild(self, items: list[tuple[float, Any]]):
        self.root = None
        self.size = 0
        for key, value in sorted(items, key=lambda x: x[0]):
            self.insert(key, value)
