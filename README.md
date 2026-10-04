# BHUMI-FUSE

BHUMI-FUSE is a 60% Smart India Hackathon prototype for PS-26013. It demonstrates one Pune urban/peri-urban case from source ingestion through discrepancy ranking and human review.

## Run

```bash
docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Vercel Demo Deployment

This repo is ready to deploy from the repository root on Vercel. The Vercel config builds the Vite app inside `frontend/` and serves `frontend/dist`.

Vercel settings:

- Framework preset: Vite
- Build command: `npm --prefix frontend install && npm --prefix frontend run build`
- Output directory: `frontend/dist`
- Install command: `npm --prefix frontend install`

For a static SIH demo, no backend environment variable is required. The frontend uses bundled static data generated from a real OpenStreetMap Overpass pull. If you later deploy a real API, set `VITE_API_URL` to that API URL.

## Demo Path

1. Source Viewer shows the mismatch between the amber simulated legal-like boundary and blue real-footprint evidence.
2. AI Boundary Extraction shows classical CV-style boundary observations and confidence.
3. Spatial Evidence Graph is interactive; click nodes to cross-filter the case.
4. Harmonized View shows RANSAC affine alignment, residual vectors, topology status, and temporal conflict classification.
5. Conflict Heatmap + Evidence Card ranks discrepancy cases and records Accept, Reject, Adjust, or Escalate decisions as new versions.
6. Export downloads a GeoJSON discrepancy export.

## Guardrails

- The app never claims AI decides land ownership or legal title.
- Source evidence is never overwritten; review actions create versioned records.
- The cadastral/ownership-like boundary is always labelled: "Simulated legal boundary - derived from real footprints, not an official record."
- Low-confidence cases route to "Needs Review / Do Not Decide."
- Every review action is timestamped and auditable through `GET /audit/{case_id}`.

## Dataset Used

The Vercel demo uses a Pune/Kharadi pilot bounding box:

```text
South: 18.5597
West:  73.7729
North: 18.56155
East:  73.77545
```

Applied datasets:

- Map background: Esri World Imagery raster tiles loaded through MapLibre.
- Real physical evidence: OpenStreetMap building footprints downloaded through the Overpass API on 2026-09-02.
- Real municipal/context evidence: OpenStreetMap road/highway ways downloaded through the Overpass API on 2026-09-02.
- GNSS/control point coordinates: points placed on real OSM road coordinates, with synthetic accuracy metadata.
- Cadastral/legal-like boundary: simulated comparison layer derived from selected real OSM building footprints. It is not an official cadastral or government record.

The included Overpass pull contains 94 OSM elements in the pilot area: 72 building footprints and 22 road/highway features.

The source cache is committed at `frontend/src/osm-pune-kharadi.json`, and the Vercel-ready dataset is generated into `frontend/src/demoData.ts`.

The scripts are included for reproducible data preparation:

```bash
python scripts/fetch_real_layers.py
python scripts/generate_simulated_cadastral.py
```

`fetch_real_layers.py` caches OSM context and writes a manifest for Microsoft/Google footprints, administrative boundaries, and current/historical imagery. `build_static_demo_data.py` converts the downloaded OSM extract into the frontend static dataset. `generate_simulated_cadastral.py` creates the only unavoidable synthetic boundary layer with a fixed seed.

## Verification Performed

- Frontend TypeScript and Vite production build: `npm run build`
- Backend Docker execution could not be run on this host because Docker CLI is not installed.
- Host Python is not installed, so backend syntax was not locally compiled outside Docker.


## DSA Course Extension

The `dsa-course-extension` branch adapts BHUMI-FUSE for the DSA course project while preserving the original SIH workflow.

### Six advanced DSA concepts added

1. **KD-Tree** — nearest GNSS/control-point lookup during harmonization.
2. **Sweep Line Algorithm** — parcel-boundary intersection detection.
3. **AVL Tree** — balanced active-status structure used by the Sweep Line.
4. **Disjoint Set Union (Union-Find)** — groups connected mismatched parcels into conflict zones.
5. **A\*** — heuristic route search for field-verification workflows.
6. **Quadtree** — hierarchical spatial indexing for map viewport rendering.

The original BHUMI-FUSE implementation already used a **SQLite R-Tree** for spatial candidate retrieval. It is retained but intentionally **not counted** among the six new course contributions.

### Where the DSA is used

- `backend/app/dsa/kd_tree.py` — KD-Tree implementation.
- `backend/app/dsa/sweep_line.py` — Sweep Line boundary-intersection engine.
- `backend/app/dsa/avl_tree.py` — AVL Tree used as the active segment structure.
- `backend/app/dsa/disjoint_set.py` — DSU with path compression and union by rank.
- `backend/app/dsa/astar.py` — A* shortest-path implementation.
- `backend/app/dsa/quadtree.py` and `frontend/src/utils/quadtree.ts` — Quadtree indexing.
- `backend/app/main.py` — integration of KD-Tree, topology diagnostics, conflict zones, A* and Quadtree API endpoints.
- `frontend/src/components/DemoMap.tsx` — viewport-based Quadtree filtering.

### DSA API endpoints

- `GET /dsa/summary` — lists the six new DSA concepts.
- `POST /dsa/astar-route` — runs A* over a weighted road graph.
- `POST /dsa/quadtree-query` — performs a Quadtree viewport query.
- `POST /validate` — now also returns Sweep Line / AVL diagnostics and DSU conflict zones.

### Current visible UI impact

The current branch keeps the original BHUMI-FUSE interface largely unchanged. The Quadtree is already used internally by the map renderer, while KD-Tree, Sweep Line, AVL Tree, DSU and A* are primarily backend integrations. A later UI pass can expose DSA-specific cards such as KD-Tree search stats, conflict-zone cards and an A* route button.

### Verification

Frontend production build:

```bash
npm run build
```

Backend DSA tests:

```bash
cd backend
python -m pytest tests/test_dsa.py -q
```

See [DSA_COURSE_EXTENSION.md](DSA_COURSE_EXTENSION.md) for architecture, complexity notes and implementation details.

## Deployment for the DSA branch

Deploy **`dsa-course-extension`**, not the original upstream branch.

### Frontend — Vercel

Repository:

```text
nidaa1308-arch/dsacp
```

Branch:

```text
dsa-course-extension
```

The existing `vercel.json` builds the Vite frontend from `frontend/`.

If a separate backend is deployed, set:

```text
VITE_API_URL=<your-backend-url>
```

### Backend — Railway

Use the same repository and branch. The existing `railway.json` starts:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

Health endpoint:

```text
/health
```

For a complete live DSA demo, both the frontend and backend must be deployed from the **same `dsa-course-extension` branch**.
