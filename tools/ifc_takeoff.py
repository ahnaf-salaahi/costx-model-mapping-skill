"""Independent quantity take-off from an IFC (for checking CostX totals).

Usage:  python ifc_takeoff.py model.ifc out.json
Needs:  pip install ifcopenshell
"""
import sys, json, math, ifcopenshell, ifcopenshell.geom
import ifcopenshell.util.element as ue, ifcopenshell.util.shape as us, ifcopenshell.util.unit as uu
f = ifcopenshell.open(sys.argv[1])
s_net = ifcopenshell.geom.settings()
s_gross = ifcopenshell.geom.settings(); s_gross.set("disable-opening-subtractions", True)

def geo(e, s):
    try: return ifcopenshell.geom.create_shape(s, e).geometry
    except Exception as ex: return None

def thickness(e):
    m = ue.get_material(e, should_skip_usage=True)
    if m and m.is_a("IfcMaterialLayerSet"):
        return sum(l.LayerThickness for l in m.MaterialLayers)/1000, [ (l.Material.Name if l.Material else None, l.LayerThickness) for l in m.MaterialLayers]
    return None, None

def mats(e):
    m = ue.get_materials(e)
    return "; ".join(sorted({x.Name for x in m if x and x.Name}))

def level(e):
    cur = e
    for _ in range(6):
        nxt = ue.get_container(cur) or ue.get_aggregate(cur)
        if nxt is None: return ""
        if nxt.is_a("IfcBuildingStorey"): return nxt.Name
        cur = nxt
    return ""

rows=[]
for e in f.by_type("IfcProduct"):
    t = e.is_a()
    if t in ("IfcBuildingStorey","IfcSite","IfcBuilding","IfcOpeningElement","IfcGrid","IfcDistributionPort","IfcAnnotation"): continue
    ty = ue.get_type(e)
    name = e.Name or ""
    fam_type = name.rsplit(":",1)[0] if name.count(":")>=2 else (ty.Name if ty else name)
    r = dict(GlobalId=e.GlobalId, IfcClass=t, Name=name, FamilyType=fam_type, Level=level(e), Materials=mats(e))
    th, layers = thickness(e)
    r["Thickness_m"] = th
    g = geo(e, s_net)
    if g is not None and t not in ("IfcSpace",):
        r["NetVolume_m3"] = us.get_volume(g)
        r["Footprint_m2"] = us.get_footprint_area(g)
        mn, mx = us.get_bbox(us.get_vertices(g))
        r["BBox_m"] = [round(mx[i]-mn[i],4) for i in range(3)]
    if t in ("IfcWall","IfcWallStandardCase"):
        gg = geo(e, s_gross)
        r["GrossVolume_m3"] = us.get_volume(gg)
        if th:
            r["NetSideArea_m2"] = r["NetVolume_m3"]/th
            r["GrossSideArea_m2"] = r["GrossVolume_m3"]/th
        r["Height_m"] = r["BBox_m"][2]
        r["Length_m"] = r["GrossSideArea_m2"]/r["Height_m"] if th and r["Height_m"] else None
        r["OpeningsArea_m2"] = (r["GrossSideArea_m2"]-r["NetSideArea_m2"]) if th else None
    if t=="IfcSlab" or t=="IfcCovering" or t=="IfcRoof":
        if th: r["Area_m2"] = r.get("NetVolume_m3",0)/th
    if t in ("IfcDoor","IfcWindow"):
        r["Width_m"] = (e.OverallWidth or 0)/1000; r["Height_m"]=(e.OverallHeight or 0)/1000
        op = ue.get_filled_void(e)
        host = op.VoidsElements[0].RelatingBuildingElement if op and op.VoidsElements else None
        r["HostWall"] = host.Name.rsplit(":",1)[0] if host else ""
    if t=="IfcSpace":
        g = geo(e, s_net)
        if g is not None:
            r["FloorArea_m2"] = us.get_footprint_area(g)
            r["Volume_m3"] = us.get_volume(g)
            mn,mx = us.get_bbox(us.get_vertices(g)); r["Height_m"]=mx[2]-mn[2]
            r["Perimeter_m"] = us.get_footprint_perimeter(g) if hasattr(us,"get_footprint_perimeter") else None
        r["RoomName"] = e.LongName; r["RoomNo"]=e.Name
        c = ue.get_container(e) or ue.get_aggregate(e)
    if t=="IfcCovering":
        sp = ue.get_container(e)
        r["Room"] = (sp.LongName + " " + sp.Name) if sp and sp.is_a("IfcSpace") else ""
    if t in ("IfcStair","IfcStairFlight"):
        p = ue.get_psets(e); sc = p.get("Pset_StairCommon") or p.get("Pset_StairFlightCommon") or {}
        r["Risers"]=sc.get("NumberOfRiser"); r["Treads"]=sc.get("NumberOfTreads")
    if t=="IfcRailing" and "BBox_m" in r:
        r["Length_m"] = math.hypot(r["BBox_m"][0], r["BBox_m"][1]) if min(r["BBox_m"][:2])>0.3 else max(r["BBox_m"][:2])
    if t=="IfcMember":
        r["Span_m"] = (ue.get_psets(e).get("Pset_MemberCommon",{}).get("Span"))
    rows.append(r)
json.dump(rows, open(sys.argv[2],"w"), indent=1, default=str)
print(len(rows))
