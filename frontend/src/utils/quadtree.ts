export type QTPoint<T = unknown> = { x: number; y: number; data: T };
export type QTRect = { minX: number; minY: number; maxX: number; maxY: number };

function contains(r: QTRect, p: QTPoint) {
  return p.x >= r.minX && p.x <= r.maxX && p.y >= r.minY && p.y <= r.maxY;
}
function intersects(a: QTRect, b: QTRect) {
  return !(b.minX > a.maxX || b.maxX < a.minX || b.minY > a.maxY || b.maxY < a.minY);
}

export class QuadTree<T = unknown> {
  bounds: QTRect;
  capacity: number;
  depth: number;
  maxDepth: number;
  points: QTPoint<T>[] = [];
  children: QuadTree<T>[] | null = null;

  constructor(bounds: QTRect, capacity = 8, depth = 0, maxDepth = 10) {
    this.bounds = bounds;
    this.capacity = capacity;
    this.depth = depth;
    this.maxDepth = maxDepth;
  }

  private split() {
    const { minX, minY, maxX, maxY } = this.bounds;
    const mx = (minX + maxX) / 2;
    const my = (minY + maxY) / 2;
    this.children = [
      new QuadTree({ minX, minY, maxX: mx, maxY: my }, this.capacity, this.depth + 1, this.maxDepth),
      new QuadTree({ minX: mx, minY, maxX, maxY: my }, this.capacity, this.depth + 1, this.maxDepth),
      new QuadTree({ minX, minY: my, maxX: mx, maxY }, this.capacity, this.depth + 1, this.maxDepth),
      new QuadTree({ minX: mx, minY: my, maxX, maxY }, this.capacity, this.depth + 1, this.maxDepth),
    ];
    const old = this.points;
    this.points = [];
    old.forEach((p) => this.insert(p));
  }

  insert(point: QTPoint<T>): boolean {
    if (!contains(this.bounds, point)) return false;
    if (this.children) return this.children.some((child) => child.insert(point));
    this.points.push(point);
    if (this.points.length > this.capacity && this.depth < this.maxDepth) this.split();
    return true;
  }

  query(area: QTRect): QTPoint<T>[] {
    if (!intersects(this.bounds, area)) return [];
    const out = this.points.filter((p) => contains(area, p));
    this.children?.forEach((child) => out.push(...child.query(area)));
    return out;
  }
}

/** Build a frontend spatial index for visible parcel centroids. */
export function buildParcelQuadTree(features: any[]) {
  const pts = features
    .map((f, i) => {
      const ring = f?.geometry?.coordinates?.[0] || [];
      if (!ring.length) return null;
      const xs = ring.map((p: number[]) => p[0]);
      const ys = ring.map((p: number[]) => p[1]);
      return {
        x: xs.reduce((a: number, b: number) => a + b, 0) / xs.length,
        y: ys.reduce((a: number, b: number) => a + b, 0) / ys.length,
        data: { feature: f, index: i },
      };
    })
    .filter(Boolean) as QTPoint<any>[];

  if (!pts.length) return null;
  const xs = pts.map((p) => p.x), ys = pts.map((p) => p.y);
  const tree = new QuadTree<any>({
    minX: Math.min(...xs), minY: Math.min(...ys),
    maxX: Math.max(...xs), maxY: Math.max(...ys),
  });
  pts.forEach((p) => tree.insert(p));
  return tree;
}
