from __future__ import annotations
import heapq, math
from typing import Any

def _heuristic(a,b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def astar_search(graph: dict[str,list[tuple[str,float]]], coords: dict[str,tuple[float,float]], start: str, goal: str):
    """A* over a weighted adjacency list. Heuristic is Euclidean distance."""
    if start not in graph or goal not in graph:
        return {"found":False,"path":[],"cost":None,"nodes_explored":0}
    pq=[(0.0,start)]
    g={start:0.0}; parent={}
    explored=0
    while pq:
        _,u=heapq.heappop(pq); explored+=1
        if u==goal:
            path=[u]
            while u in parent:
                u=parent[u]; path.append(u)
            path.reverse()
            return {"found":True,"path":path,"cost":round(g[goal],4),"nodes_explored":explored}
        for v,w in graph.get(u,[]):
            cand=g[u]+w
            if cand < g.get(v,float("inf")):
                g[v]=cand; parent[v]=u
                h=_heuristic(coords.get(v,(0,0)), coords.get(goal,(0,0)))
                heapq.heappush(pq,(cand+h,v))
    return {"found":False,"path":[],"cost":None,"nodes_explored":explored}
