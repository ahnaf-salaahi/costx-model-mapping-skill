# Troubleshooting (every item seen in real use)

### Revit / IFC
| Problem | Cause | Fix |
|---|---|---|
| "Can't open" a Revit file | Saved in a newer Revit | Install that version (free education licence) or ask the author for an IFC. You cannot save down. |
| Can't tick boxes in IFC export setup | Built-in `<...>` setups are locked | Duplicate the setup, then edit the copy. |
| No "Property Sets" tab | Revit 2025+ | General tab → Property Mapping → "…". |
| CostX properties show no NetArea etc. | Base quantities not exported | Tick *Export base quantities*, re-export, and check with `tools/check_ifc.py`. |
| Descriptions still old after re-export | Edited instance Properties, not the type | Edit Type → Identity Data → Description → **Apply** → OK. |
| IFC header says a newer Revit | Model was saved/exported from that version | The .rvt now needs that version. |

### Model Map editor
| Problem | Fix |
|---|---|
| Preview shows 0 | Put the property in the **Area/Length/Volume** field (scroll below ZC8). *Dimension* is only a label. |
| Field goes red | Text not in quotes, missing `&`, or `IIF`. Use `IF`. |
| Typed text vanished | Field not committed. Double-click the field, type, then click another field. |
| "Dimension group … has a blank folder" | An instance under the type has its own partial mapping (bold). Complete or clear it. |
| "Ambiguous property Name" warning | Rooms have two Name properties. Use `[LongName]`. |
| Mapping landed on the wrong node | The tree expanded/scrolled after a click. Re-screenshot before each click; clear the wrong node's fields. |
| Element has blank level, lands in an empty folder | Map that instance with a fixed level in its folder. |
| Edit button does nothing | Select the map row, then click Edit and wait ~5 s. |

### Import
| Problem | Fix |
|---|---|
| Only a few elements imported | Click **Show All Objects** before importing. |
| Duplicate groups with "(folder)" suffix | Re-import never updates; it adds. Right-click the old folders → Delete Folder, then import again. |
| Delete key doesn't remove a group | Use right-click → Delete Dimension Group / Delete Folder. |
| Hand-measured groups disappeared | They aren't touched by import. Check you didn't delete their folder. |

### Quantity sanity checks (from the test project)
- Roof `BaseQuantities.NetArea` was 4.11 m² for a 44.29 m² slope, so use **GrossArea**.
- First-floor slab `BaseQuantities.NetArea` 80.60 m² vs Revit `Area` 75.54 m² (stair hole), so use **[Area]**.
- 3 partitions exported as `IfcWall` had GrossSideArea 10.7 m² vs real 17.4 m², so use **[Area]**.
- Stair handrail Revit Length 4.81 m vs a geometry estimate of 1.85 m, so use **[Length]**.
