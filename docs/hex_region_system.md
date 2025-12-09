# Faerun Hex Region System - Design Document

## Overview

The Faerun hex map uses a fixed 60-mile hex grid overlaid on the Forgotten Realms. Each hex has a base region type, can be a special fixed location, and may have event modifiers that affect encounters and presentation.

**Map Source:** `D:\Code\Faerun\assets\60_mile_map.jpg`

---

## System Architecture

```
Hex = Base Region + Special Type (optional) + Event Modifier (optional)
```

### Hierarchy
1. **Base Region** (required): Determines default monsters, terrain, backdrop
2. **Special Hex** (optional): Overrides region for fixed locations (cities, dungeons)
3. **Event Modifier** (optional): Temporarily modifies encounters and backdrop

---

## Regional Zones (Base Layer)

### 1. Countryside
**Description:** Temperate lands, farms, forests, typical Faerûn terrain

**Hex Types:**
- Plains
- Forest
- Hills
- Urban (small settlements)

**Monster Groups:**
- Beasts (wolves, bears, boars)
- Humanoids (bandits, goblins, orcs)
- Fey (in forests)
- Undead (ruins, graveyards)

**Encounter Types:**
- Wandering monsters
- Bandit ambushes
- Wild animal attacks
- Local threats

**Backdrop:** Rolling hills, deciduous forests, farmland

---

### 2. Icewind Dale
**Description:** Frozen tundra, harsh arctic wasteland

**Hex Types:**
- Arctic/Tundra
- Mountains (Spine of the World)
- Frozen lakes
- Ice caves

**Monster Groups:**
- Arctic beasts (polar bears, yeti, winter wolves)
- Giants (frost giants, ice trolls)
- Elementals (ice/air)
- Aberrations (remorhaz)

**Encounter Types:**
- Survival challenges (blizzards)
- Territorial predators
- Giant raiding parties
- Ancient horrors

**Backdrop:** Snow-covered peaks, ice fields, aurora borealis, driving snow

---

### 3. Moonshae Isles
**Description:** Celtic-inspired islands, mystical forests

**Hex Types:**
- Coastal
- Ancient forests
- Rocky highlands
- Moorlands

**Monster Groups:**
- Fey (pixies, sprites, treants)
- Beasts (deer, wolves, sea creatures)
- Humanoids (druids, northlanders)
- Undead (haunted barrows)

**Encounter Types:**
- Fey encounters (tricks, bargains)
- Natural guardians
- Ancient spirits
- Coastal raiders

**Backdrop:** Misty forests, standing stones, sea cliffs, Celtic ruins

---

### 4. Calimshan
**Description:** Desert empire, Arabian Nights aesthetic

**Hex Types:**
- Desert (sandy)
- Oases
- Rocky badlands
- Ancient ruins

**Monster Groups:**
- Elementals (fire, earth, djinn, efreet)
- Monstrosities (giant scorpions, sphinxes)
- Humanoids (bandits, slavers)
- Undead (mummies, tomb guardians)

**Encounter Types:**
- Desert survival
- Elemental manifestations
- Treasure hunters
- Ancient curses

**Backdrop:** Sand dunes, palm oases, sandstorms, ancient ziggurats

---

## Special Hexes (Fixed Locations)

Special hexes are marked on the map and override the base region's encounter generation.

### City
**Visibility:** Always visible on map
**Examples:** Waterdeep, Baldur's Gate, Neverwinter, Luskan

**Properties:**
- No random encounters (controlled environment)
- Urban terrain/backdrop
- Access to vendors, quests, safe rests
- City-specific NPCs and events

**Monster Groups (if combat occurs):**
- City guards
- Criminals/thieves
- Constructs (in wizard towers)
- Urban monsters (wererats, vampires)

**Encounter Types:**
- Plot-driven only
- Investigation/intrigue
- Arena/sanctioned combat
- Criminal encounters

**Backdrop:** City streets, market squares, taverns, city walls

---

### Dungeon
**Visibility:** Visible on map (known locations)
**Examples:** Undermountain, Tomb of Horrors, ancient ruins

**Properties:**
- Fixed encounter tables
- Indoor terrain
- Treasure/loot focus
- Multi-level structure

**Monster Groups:**
- Dungeon-specific (varies by location)
- Undead (tombs)
- Aberrations (deep dungeons)
- Constructs (wizard dungeons)
- Dragons (lairs)

**Encounter Types:**
- Room-by-room encounters
- Traps and hazards
- Boss encounters
- Treasure rooms

**Backdrop:** Stone corridors, torch-lit chambers, ancient architecture, darkness

---

## Event Hex Modifiers (Temporary Overlays)

Events are temporary conditions that modify a hex's encounters and presentation. Multiple events can potentially stack.

### Undead Infestation
**Duration:** Persists until cleared
**Trigger:** Necromancer activity, ancient curse, death of many

**Modifications:**
- **Monster Override:** 75% chance encounters are undead
- **Backdrop Modifier:** Fog, gray skies, dead vegetation, ravens
- **Terrain Effect:** Movement cost +20% (corpses, fear)
- **Special:** Necrotic damage has advantage

**Monster Groups:**
- Zombies, skeletons (low level)
- Ghouls, wights (mid level)
- Wraiths, vampires (high level)
- Liches, death knights (legendary)

**Encounter Types:**
- Hordes of undead
- Necromancer encounters
- Haunted locations
- Cursed objects

---

### Demonic Portal
**Duration:** Until portal closed (quest objective)
**Trigger:** Ritual gone wrong, planar instability

**Modifications:**
- **Monster Override:** 90% chance encounters are fiends
- **Backdrop Modifier:** Red sky, sulfur smell, reality tears, floating debris
- **Terrain Effect:** Fire/necrotic hazards
- **Special:** Fiends have temp HP bonus

**Monster Groups:**
- Imps, quasits (scouts)
- Demons (various types)
- Devils (organized)
- Demon lords (legendary)

**Encounter Types:**
- Demon patrols
- Corrupted wildlife
- Cultist rituals
- Portal guardians

---

### Marauders
**Duration:** Until driven off or defeated
**Trigger:** War, famine, mercenary contracts

**Modifications:**
- **Monster Override:** 80% humanoid encounters
- **Backdrop Modifier:** Smoke from fires, destroyed buildings, refugees
- **Terrain Effect:** Difficult terrain (rubble, barricades)
- **Special:** Humanoids use tactics, have better equipment

**Monster Groups:**
- Bandits (organized)
- Mercenaries
- Orcs/goblins (war bands)
- Evil humanoids (drow, duergar)

**Encounter Types:**
- Raiding parties
- Ambushes on roads
- Fortified camps
- War chief encounters

---

### Legendary Creature
**Duration:** Until creature defeated or driven off
**Trigger:** Dragon awakens, ancient beast emerges

**Modifications:**
- **Monster Override:** 50% chance of legendary creature or its minions
- **Backdrop Modifier:** Themed to creature (dragon = scorched earth, etc.)
- **Terrain Effect:** Lair actions in effect
- **Special:** Legendary saves, lair-wide effects

**Monster Groups:**
- Legendary creature itself
- Creature's minions/cultists
- Attracted predators
- Territorial defenders

**Encounter Types:**
- Legendary creature sighting (flee or fight)
- Minion patrols
- Lair encounters
- Territorial warnings

---

## Data Structure Example

```json
{
  "hex_id": "Q12_R8",
  "base_region": "Countryside",
  "base_terrain": "forest",
  "special_type": null,
  "events": ["Undead Infestation"],
  "encounter_override": {
    "monster_groups": ["undead"],
    "backdrop": "fog_forest_undead"
  }
}
```

---

## Priority System

When generating encounters:
1. **Event Modifiers** (highest priority if present)
2. **Special Hex Type** (if city or dungeon)
3. **Base Region** (default fallback)

## Visual System

**Backdrop Assets Needed:**
- Countryside: `countryside_plains.jpg`, `countryside_forest.jpg`, etc.
- Icewind: `icewind_tundra.jpg`, `icewind_mountains.jpg`, etc.
- Moonshae: `moonshae_forest.jpg`, `moonshae_coast.jpg`, etc.
- Calimshan: `calimshan_desert.jpg`, `calimshan_oasis.jpg`, etc.
- Events: `undead_modifier.png` (overlay), `demonic_portal.png`, etc.
- Cities: `waterdeep.jpg`, `baldurs_gate.jpg`, etc.
- Dungeons: `dungeon_corridor.jpg`, `dungeon_chamber.jpg`, etc.
