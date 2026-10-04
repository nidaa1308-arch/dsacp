# BHUMI-FUSE — DSA Course Extension

This branch keeps the shortlisted SIH BHUMI-FUSE workflow intact and adds six advanced DSA concepts that are separate from the project's pre-existing SQLite R-Tree.

## New DSA concepts

1. **KD-Tree** — balanced 2-D nearest-neighbour search for GNSS/control points.
2. **Sweep Line** — event-ordered parcel-boundary intersection detection.
3. **AVL Tree** — balanced active-segment structure used by the Sweep Line.
4. **Disjoint Set Union** — conflict-zone grouping with path compression and union by rank.
5. **A\*** — heuristic shortest-path search for field verification routing.
6. **Quadtree** — hierarchical spatial partitioning for map viewport queries.

## Existing DSA retained

The original project already contained a **SQLite R-Tree** in `backend/app/db.py`. It is retained for candidate spatial filtering and is **not claimed as a new course contribution**.

## Integration points

- `backend/app/main.py`
  - KD-Tree replaces brute-force nearest GNSS scanning in harmonization.
  - `/validate` now returns Sweep Line + AVL intersection diagnostics and DSU conflict zones.
  - `POST /dsa/astar-route` exposes A* routing.
  - `POST /dsa/quadtree-query` exposes Quadtree viewport queries.
  - `GET /dsa/summary` documents the six course DSA modules.
- `frontend/src/utils/quadtree.ts`
  - Reusable client-side Quadtree for visible parcel indexing.

## Complexity summary

| DSA | Main operation | Typical complexity |
|---|---|---|
| KD-Tree | nearest neighbour | average O(log n) |
| Sweep Line | segment intersections | O((n+k) log n) target form |
| AVL Tree | insert/delete/search | O(log n) |
| DSU | union/find | amortized O(alpha(n)) |
| A* | route search | graph dependent; guided by heuristic |
| Quadtree | regional query | sublinear average for well-distributed spatial data |

## Run tests

From `backend/`:

```bash
pytest tests/test_dsa.py
```

If pytest is not installed:

```bash
pip install pytest
```
