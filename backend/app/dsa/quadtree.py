from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class Rect:
    min_x: float; min_y: float; max_x: float; max_y: float
    def contains(self,p):
        x,y=p; return self.min_x<=x<=self.max_x and self.min_y<=y<=self.max_y
    def intersects(self,o):
        return not (o.min_x>self.max_x or o.max_x<self.min_x or o.min_y>self.max_y or o.max_y<self.min_y)

class QuadTree:
    """Point Quadtree for fast viewport queries and map partitioning."""
    def __init__(self,bounds:Rect,capacity=8,depth=0,max_depth=10):
        self.bounds=bounds; self.capacity=capacity; self.depth=depth; self.max_depth=max_depth
        self.items=[]; self.children=None

    def _split(self):
        b=self.bounds; mx=(b.min_x+b.max_x)/2; my=(b.min_y+b.max_y)/2
        self.children=[
            QuadTree(Rect(b.min_x,b.min_y,mx,my),self.capacity,self.depth+1,self.max_depth),
            QuadTree(Rect(mx,b.min_y,b.max_x,my),self.capacity,self.depth+1,self.max_depth),
            QuadTree(Rect(b.min_x,my,mx,b.max_y),self.capacity,self.depth+1,self.max_depth),
            QuadTree(Rect(mx,my,b.max_x,b.max_y),self.capacity,self.depth+1,self.max_depth),
        ]
        old=self.items; self.items=[]
        for item in old: self.insert(*item)

    def insert(self,point,payload):
        if not self.bounds.contains(point): return False
        if self.children:
            return any(ch.insert(point,payload) for ch in self.children)
        self.items.append((point,payload))
        if len(self.items)>self.capacity and self.depth<self.max_depth:
            self._split()
        return True

    def query(self,area:Rect):
        if not self.bounds.intersects(area): return []
        out=[payload for point,payload in self.items if area.contains(point)]
        if self.children:
            for ch in self.children: out.extend(ch.query(area))
        return out

    def stats(self):
        if not self.children:
            return {"nodes":1,"leaves":1,"items":len(self.items),"max_depth":self.depth}
        stats=[c.stats() for c in self.children]
        return {
            "nodes":1+sum(s["nodes"] for s in stats),
            "leaves":sum(s["leaves"] for s in stats),
            "items":sum(s["items"] for s in stats),
            "max_depth":max(s["max_depth"] for s in stats),
        }
