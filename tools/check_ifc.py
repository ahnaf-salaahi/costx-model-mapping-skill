"""Pre-flight check of an IFC before CostX model mapping.

Usage:  python check_ifc.py model.ifc
Needs:  pip install ifcopenshell
"""
import sys
import collections
import ifcopenshell
import ifcopenshell.util.element as ue

SKIP = {"IfcOpeningElement", "IfcBuildingStorey", "IfcSite", "IfcBuilding",
        "IfcDistributionPort", "IfcGrid", "IfcAnnotation"}


def main(path):
    f = ifcopenshell.open(path)
    print(f"File: {path}  Schema: {f.schema}")
    try:
        print(f"Exported by: {f.header.file_name.originating_system}")
    except Exception:
        pass

    nq = len(f.by_type("IfcElementQuantity"))
    print(f"\nBase quantity sets: {nq}  ->  "
          + ("OK" if nq else "MISSING: re-export with 'Export base quantities' ticked"))

    print("\nStoreys (use these in level expressions):")
    for s in f.by_type("IfcBuildingStorey"):
        print(f"  {s.Name}  elev {s.Elevation}")

    print("\nElements per class:")
    c = collections.Counter(e.is_a() for e in f.by_type("IfcProduct") if e.is_a() not in SKIP)
    for k, v in c.most_common():
        print(f"  {k:28s} {v}")

    issues = []
    for e in f.by_type("IfcWall"):
        mats = {m.Name for m in ue.get_materials(e) if m}
        ps = ue.get_psets(e)
        name = (e.Name or "").rsplit(":", 1)[0]
        if "Interior" in name or "Partition" in name:
            if (ps.get("Pset_WallCommon") or {}).get("IsExternal"):
                issues.append(f"Partition flagged IsExternal=True: {name} (set type Function = Interior)")
        for m in mats:
            if m.lower() in {"aluminum", "aluminium", "default wall", "<unnamed>"}:
                issues.append(f"Suspicious wall material '{m}': {name}")
    for sp in f.by_type("IfcSpace"):
        if not sp.LongName or sp.LongName.strip().lower() == "room name":
            issues.append(f"Unnamed room {sp.Name}")
    for cls in ("IfcFooting", "IfcColumn", "IfcBeam"):
        if not f.by_type(cls):
            issues.append(f"No {cls} in model: measure manually from drawings")
    proxies = collections.Counter((e.Name or "").rsplit(":", 1)[0]
                                  for e in f.by_type("IfcBuildingElementProxy"))
    if proxies:
        issues.append("Proxies (decide map/skip): " + ", ".join(f"{k} x{v}" for k, v in proxies.items()))

    print("\nIssues / notes:")
    for i in sorted(set(issues)):
        print("  -", i)
    if not issues:
        print("  none")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
