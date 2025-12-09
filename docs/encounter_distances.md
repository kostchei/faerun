# Encounter Distance Reference

## Distance Formulas by Terrain

Based on visibility and line of sight from dnd-encounters-24 app.

| Terrain | Formula | Average | Range |
|---------|---------|---------|-------|
| **Plains** | 6d6 × 10 ft | 210 ft | 60-360 ft |
| **Desert** | 6d6 × 10 ft | 210 ft | 60-360 ft |
| **Mountains** | 4d10 × 10 ft | 220 ft | 40-400 ft |
| **Hills** | 2d10 × 10 ft | 110 ft | 20-200 ft |
| **Urban** | 2d10 × 10 ft | 110 ft | 20-200 ft |
| **Forest** | 2d8 × 10 ft | 90 ft | 20-160 ft |
| **Swamp** | 2d6 × 10 ft | 70 ft | 20-120 ft |

## Usage

When an encounter is generated, the system automatically calculates the starting distance based on the terrain where the encounter occurs. This distance represents how far away the party spots the encounter when it begins.

**API Response includes:**
```json
{
  "encounter_distance_ft": 80,
  "terrain_type": "swamp"
}
```

## Tactical Implications

- **Long distances** (200+ ft): Party has time to prepare, buff, or retreat
- **Medium distances** (90-200 ft): Standard combat engagement range
- **Short distances** (20-90 ft): Limited reaction time, ambush potential
- **Visibility**: High visibility terrains (plains, desert, mountain) have longer average distances
- **Cover**: Low visibility terrains (forest, swamp) favor surprise and close encounters
