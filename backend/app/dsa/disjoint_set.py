from __future__ import annotations

class DisjointSet:
    """Union-Find with path compression and union by rank."""
    def __init__(self, items=()):
        self.parent={}
        self.rank={}
        for x in items: self.add(x)

    def add(self,x):
        if x not in self.parent:
            self.parent[x]=x; self.rank[x]=0

    def find(self,x):
        self.add(x)
        if self.parent[x] != x:
            self.parent[x]=self.find(self.parent[x])
        return self.parent[x]

    def union(self,a,b):
        ra,rb=self.find(a),self.find(b)
        if ra==rb: return ra
        if self.rank[ra] < self.rank[rb]: ra,rb=rb,ra
        self.parent[rb]=ra
        if self.rank[ra]==self.rank[rb]: self.rank[ra]+=1
        return ra

    def groups(self):
        out={}
        for x in list(self.parent):
            out.setdefault(self.find(x),[]).append(x)
        return list(out.values())

def conflict_zones(residuals, adjacency_pairs, min_risk=("high","medium")):
    flagged={r.get("parcel_id","").replace("parcel-","") for r in residuals if r.get("risk") in min_risk}
    dsu=DisjointSet(flagged)
    for a,b in adjacency_pairs:
        a=str(a).replace("parcel-",""); b=str(b).replace("parcel-","")
        if a in flagged and b in flagged:
            dsu.union(a,b)
    zones=[]
    by_id={str(r.get("parcel_id","")).replace("parcel-",""):r for r in residuals}
    for idx,members in enumerate(sorted(dsu.groups(), key=lambda g:(-len(g),g)),1):
        vals=[by_id[m].get("residual_m") for m in members if m in by_id and by_id[m].get("residual_m") is not None]
        zones.append({
            "zone_id":f"CZ-{idx:02d}",
            "parcels":sorted(members),
            "parcel_count":len(members),
            "max_residual_m":round(max(vals),2) if vals else None,
            "avg_residual_m":round(sum(vals)/len(vals),2) if vals else None,
        })
    return zones
