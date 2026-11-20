# Ready-to-paste Model Map expressions (CostX 7, tested)

Copy into the field named in each heading. Replace the Dimension Group text to suit your
project. Leave every unlisted field blank.

## Ceilings: `IfcCovering` → type node
| Field | Value |
|---|---|
| Folder | `"3 SUPERSTRUCTURE\" & [Level] & "\20 CEILINGS"` |
| Dimension Group | `"Ceiling - 16mm GWB on timber furring"` |
| Measure Type | Area |
| Dimension | `[Name]` |
| Area | `[BaseQuantities.NetArea]` |

## Doors: `IfcDoor` class node
| Folder | `"3 SUPERSTRUCTURE\" & [Level] & "\24 DOORS"` |
|---|---|
| Dimension Group | `[Family and Type]` |
| Measure Type | Count |
| Dimension | `[Name]` |

## Windows: `IfcWindow` class node
| Folder | `"3 SUPERSTRUCTURE\" & [Level] & "\23 WINDOWS"` |
|---|---|
| Dimension Group | `[Family and Type]` |
| Measure Type | Count |
| Dimension | `[Family and Type]` |

## Sanitary: `IfcFlowTerminal` class node
| Folder | `"3 SUPERSTRUCTURE\" & [Level] & "\32 SANITARY FITTINGS"` |
|---|---|
| Dimension Group | `[Family and Type]` |
| Measure Type | Count |

## Railings: `IfcRailing` class node
| Folder | `"3 SUPERSTRUCTURE\" & [Base Level] & "\25 STAIRS AND BALUSTRADES"` |
|---|---|
| Dimension Group | `[Family and Type]` |
| Measure Type | Length |
| Dimension | `[Name]` |
| Length | `[Length]` |

Stair handrail instance with blank Base Level, mapped on the **instance** node:
| Folder | `"3 SUPERSTRUCTURE\L1\25 STAIRS AND BALUSTRADES"` |
|---|---|
| Length | `[Length]` |

## Roof: `IfcSlab` → Basic Roof type node
| Folder | `"3 SUPERSTRUCTURE\L3 ROOF\18 ROOF COVERINGS"` |
|---|---|
| Dimension Group | `"Roof covering - measured on slope"` |
| Measure Type | Area |
| Area | `[BaseQuantities.GrossArea]` |
| Volume | `[BaseQuantities.GrossVolume]` |

## Floor slabs: `IfcSlab` → Floor type node
| Folder | `IF([Level]="L1","2 SUBSTRUCTURE\11 IN-SITU CONCRETE","3 SUPERSTRUCTURE\" & [Level] & "\11 IN-SITU CONCRETE")` |
|---|---|
| Dimension Group | `"RC slab 150mm - " & [Level]` |
| Measure Type | Volume |
| Dimension | `[Name]` |
| Length | `[BaseQuantities.Perimeter]` |
| Area | `[Area]` |
| Volume | `[BaseQuantities.NetVolume]` |

## Rooms: `IfcSpace` class node
| Folder | `"3 SUPERSTRUCTURE\" & [Level] & "\28 FLOOR FINISHES"` |
|---|---|
| Dimension Group | `"Floor finish - room areas"` |
| Measure Type | Area |
| Dimension | `[LongName]` |
| Length | `[BaseQuantities.GrossPerimeter]` |
| Area | `[BaseQuantities.NetFloorArea]` |

## Stair: `IfcStair` class node
| Folder | `"3 SUPERSTRUCTURE\L1\25 STAIRS AND BALUSTRADES"` |
|---|---|
| Dimension Group | `"Steel plate-stringer staircase, 20 risers"` |
| Measure Type | Count |
| Dimension | `"Staircase"` |

## Walls: each Family:Type under `IfcWallStandardCase` AND `IfcWall`
| Folder | `"3 SUPERSTRUCTURE\" & [Base Constraint] & "\14 MASONRY"` |
|---|---|
| Dimension Group | `"Wall - 230mm common brickwork, external"` (or the partition name; use the same name in both classes) |
| Measure Type | Area |
| Dimension | `[Family and Type]` |
| Length | `[Length]` |
| Area | `[Area]` |
| Volume | `[BaseQuantities.NetVolume]` |

## Paving: each toposolid path **instance**
| Folder | `"4 EXTERNAL WORKS\35 SITE WORKS"` |
|---|---|
| Dimension Group | `"Paving - 350mm asphalt path"` |
| Measure Type | Area |
| Dimension | `"Asphalt path"` |
| Area | `[Area]` |

## Useful extras
- Volume converted to area for a wall without side area: `[BaseQuantities.NetVolume]/0.115`
- Zone instead of folder for levels: put `[Level]` in **ZC1**, then rename Zone Category 1
  to "Level" (Dimensions ribbon → Zones).
