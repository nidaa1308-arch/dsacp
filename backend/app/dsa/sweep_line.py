from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .avl_tree import AVLTree

@dataclass
class Segment:
    a: tuple[float, float]
    b: tuple[float, float]
    parcel_id: str
    edge_index: int

    @property
    def left(self):
        return self.a if self.a[0] <= self.b[0] else self.b
    @property
    def right(self):
        return self.b if self.a[0] <= self.b[0] else self.a

def _orient(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def _intersects(s1: Segment, s2: Segment):
    if s1.parcel_id == s2.parcel_id:
        return False
    a,b,c,d = s1.a,s1.b,s2.a,s2.b
    o1,o2,o3,o4 = _orient(a,b,c),_orient(a,b,d),_orient(c,d,a),_orient(c,d,b)
    return (o1 == 0 or o2 == 0 or o1 * o2 < 0) and (o3 == 0 or o4 == 0 or o3 * o4 < 0)

def _y_at(seg: Segment, x: float):
    x1,y1 = seg.a; x2,y2 = seg.b
    if abs(x2-x1) < 1e-12:
        return min(y1,y2)
    t=(x-x1)/(x2-x1)
    return y1+t*(y2-y1)

def polygon_segments(features: list[dict[str, Any]]):
    out=[]
    for i, feat in enumerate(features):
        pid=str(feat.get("properties",{}).get("parcel_id", i))
        coords=feat.get("geometry",{}).get("coordinates",[])
        if not coords: continue
        ring=coords[0]
        for j in range(len(ring)-1):
            out.append(Segment(tuple(ring[j][:2]), tuple(ring[j+1][:2]), pid, j))
    return out

def sweep_intersections(features: list[dict[str, Any]]):
    """Bentley-Ottmann style sweep skeleton using an AVL active-status tree."""
    segments=polygon_segments(features)
    events=[]
    for s in segments:
        events.append((s.left[0],0,s.left[1],s))
        events.append((s.right[0],1,s.right[1],s))
    events.sort(key=lambda e:(e[0],e[1],e[2]))
    active=[]
    tree=AVLTree()
    found=set()
    checks=0

    for x,kind,_,seg in events:
        if kind==0:
            active.append(seg)
        else:
            active=[s for s in active if s is not seg]

        tree.rebuild([(_y_at(s,x),s) for s in active])
        ordered=[v for _,v in tree.inorder()]
        for i in range(len(ordered)-1):
            s1,s2=ordered[i],ordered[i+1]
            checks += 1
            if _intersects(s1,s2):
                key=tuple(sorted((s1.parcel_id,s2.parcel_id)))
                found.add(key)

    return {
        "intersections":[{"parcel_a":a,"parcel_b":b} for a,b in sorted(found)],
        "intersection_pairs":len(found),
        "segments":len(segments),
        "events":len(events),
        "neighbour_checks":checks,
        "active_structure":"AVL Tree",
    }
