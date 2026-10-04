from app.dsa.kd_tree import KDTree
from app.dsa.avl_tree import AVLTree
from app.dsa.disjoint_set import DisjointSet
from app.dsa.astar import astar_search
from app.dsa.quadtree import QuadTree, Rect
from app.dsa.sweep_line import sweep_intersections


def test_kdtree_nearest():
    tree = KDTree([((0.0, 0.0), "A"), ((5.0, 5.0), "B"), ((2.0, 2.0), "C")])
    result = tree.nearest((1.8, 2.1))
    assert result["payload"] == "C"


def test_avl_sorted():
    t = AVLTree()
    for k in [3, 2, 1, 4, 5]:
        t.insert(k, str(k))
    assert [k for k, _ in t.inorder()] == [1, 2, 3, 4, 5]


def test_dsu_groups():
    d = DisjointSet(["1", "2", "3"])
    d.union("1", "2")
    groups = [set(g) for g in d.groups()]
    assert {"1", "2"} in groups
    assert {"3"} in groups


def test_astar():
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("A", 1), ("C", 1)],
        "C": [("A", 4), ("B", 1)],
    }
    coords = {"A": (0, 0), "B": (1, 0), "C": (2, 0)}
    result = astar_search(graph, coords, "A", "C")
    assert result["found"]
    assert result["path"] == ["A", "B", "C"]


def test_quadtree():
    q = QuadTree(Rect(0, 0, 10, 10), capacity=1)
    q.insert((1, 1), "A")
    q.insert((9, 9), "B")
    assert q.query(Rect(0, 0, 5, 5)) == ["A"]


def test_sweep_line_detects_cross_parcel_intersection():
    features = [
        {"geometry": {"type": "Polygon", "coordinates": [[[0,0],[2,0],[2,2],[0,2],[0,0]]]},
         "properties": {"parcel_id": "1"}},
        {"geometry": {"type": "Polygon", "coordinates": [[[1,-1],[3,-1],[3,1],[1,1],[1,-1]]]},
         "properties": {"parcel_id": "2"}},
    ]
    result = sweep_intersections(features)
    assert result["intersection_pairs"] >= 1
