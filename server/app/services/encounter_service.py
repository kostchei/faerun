"""
Path: server/app/services/encounter_service.py
Purpose: Core encounter generation logic for the game
Logic:
  - Generates encounters based on position, terrain, and party level
  - Uses deterministic seed-based generation for consistency
  - Calculates CR based on distance and terrain difficulty
  - Maps terrain types to appropriate creature types
  - Based on TaleKeeper's encounter generation system
"""

import random
from typing import Dict, List, Optional
from enum import Enum
from .hex_coordinate_system import HexCoordinateSystem
from .terrain_service import TerrainService, TerrainType


class EncounterType(str, Enum):
    """Types of encounters that can be generated"""
    BEAST = "beast"
    HUMANOID = "humanoid"
    MONSTROSITY = "monstrosity"
    UNDEAD = "undead"
    DRAGON = "dragon"
    GIANT = "giant"
    FEY = "fey"
    ELEMENTAL = "elemental"
    ABERRATION = "aberration"
    FIEND = "fiend"
    CONSTRUCT = "construct"


class EncounterService:
    """
    Service for generating and managing combat encounters.
    Provides deterministic encounter generation based on location and party state.
    """

    # Mapping of terrain types to likely encounter types
    TERRAIN_ENCOUNTER_TYPES = {
        TerrainType.PLAINS: [EncounterType.BEAST, EncounterType.HUMANOID],
        TerrainType.FOREST: [EncounterType.BEAST, EncounterType.FEY, EncounterType.HUMANOID],
        TerrainType.MOUNTAIN: [EncounterType.GIANT, EncounterType.DRAGON, EncounterType.BEAST],
        TerrainType.HILLS: [EncounterType.HUMANOID, EncounterType.BEAST, EncounterType.GIANT],
        TerrainType.SWAMP: [EncounterType.MONSTROSITY, EncounterType.UNDEAD, EncounterType.ABERRATION],
        TerrainType.DESERT: [EncounterType.MONSTROSITY, EncounterType.ELEMENTAL, EncounterType.BEAST],
        TerrainType.URBAN: [EncounterType.HUMANOID, EncounterType.CONSTRUCT],
    }

    def __init__(self):
        self.coord_system = HexCoordinateSystem()
        self.terrain_service = TerrainService()

    def generate_encounter(
        self,
        q: int,
        r: int,
        terrain_type: TerrainType,
        party_level: int = 1
    ) -> Optional[Dict]:
        """
        Generate an encounter for a specific hex location.
        
        Args:
            q, r: Hex coordinates
            terrain_type: The terrain at this location
            party_level: Average party level for CR scaling
            
        Returns:
            Encounter data dict if encounter occurs, None otherwise
        """
        # Get position seed for deterministic generation
        seed = self._get_position_seed(q, r)
        random.seed(seed)

        # Check if encounter occurs based on terrain rate
        encounter_rate = self.terrain_service.get_encounter_rate(terrain_type)
        if random.random() >= encounter_rate:
            return None

        # Calculate encounter CR based on distance and terrain
        distance = self.coord_system.get_distance(0, 0, q, r)
        cr = self._calculate_encounter_cr(distance, terrain_type, party_level)

        # Determine encounter type based on terrain
        encounter_type = self._get_encounter_type_for_terrain(terrain_type)

        # Calculate encounter starting distance (visibility-based)
        encounter_distance = self.terrain_service.calculate_encounter_distance(terrain_type)

        # Generate encounter description
        description = self._generate_encounter_description(encounter_type, terrain_type, cr)

        return {
            'q': q,
            'r': r,
            'terrain_type': terrain_type.value,
            'encounter_type': encounter_type.value,
            'cr': cr,
            'description': description,
            'distance_from_origin': distance,
            'encounter_distance_ft': encounter_distance,
            'seed': seed,
        }


    def _calculate_encounter_cr(
        self,
        distance: int,
        terrain_type: TerrainType,
        party_level: int
    ) -> int:
        """
        Calculate the Challenge Rating for an encounter.
        
        Based on TaleKeeper's formula:
        - Base CR = distance // 3
        - Terrain modifier for difficult terrain
        - Adjusted for party level
        
        Args:
            distance: Distance from origin in hex units
            terrain_type: The terrain type
            party_level: Average party level
            
        Returns:
            Challenge Rating (0-20)
        """
        # Base CR from distance (from TaleKeeper)
        base_cr = distance // 3

        # Terrain modifiers
        if terrain_type in [TerrainType.MOUNTAIN, TerrainType.SWAMP]:
            base_cr += 1

        # Scale with party level (ensure encounters are appropriate)
        # Lower bound: party_level - 2, Upper bound: party_level + 2
        min_cr = max(0, party_level - 2)
        max_cr = party_level + 2

        # Clamp CR to reasonable range
        cr = max(min_cr, min(base_cr, max_cr))
        
        return max(0, min(cr, 20))  # Cap at CR 20

    def _get_encounter_type_for_terrain(self, terrain_type: TerrainType) -> EncounterType:
        """
        Select an appropriate encounter type for the terrain.
        
        Args:
            terrain_type: The terrain type
            
        Returns:
            An EncounterType value
        """
        possible_types = self.TERRAIN_ENCOUNTER_TYPES.get(
            terrain_type,
            [EncounterType.BEAST]
        )
        return random.choice(possible_types)

    def _get_position_seed(self, q: int, r: int) -> int:
        """
        Generate a deterministic seed from hex coordinates.
        
        Args:
            q, r: Hex coordinates
            
        Returns:
            Integer seed value
        """
        return hash(f"{q},{r}") % (2**31)

    def _generate_encounter_description(
        self,
        encounter_type: EncounterType,
        terrain_type: TerrainType,
        cr: int
    ) -> str:
        """
        Generate a narrative description for the encounter.
        
        Args:
            encounter_type: Type of encounter
            terrain_type: Terrain where encounter occurs
            cr: Challenge rating
            
        Returns:
            Descriptive text
        """
        # Template descriptions based on encounter and terrain
        templates = {
            EncounterType.BEAST: {
                TerrainType.PLAINS: f"A pack of wild beasts roams the grasslands (CR {cr})",
                TerrainType.FOREST: f"Predators stalk through the dense forest (CR {cr})",
                TerrainType.MOUNTAIN: f"Mountain predators prowl the rocky slopes (CR {cr})",
            },
            EncounterType.HUMANOID: {
                TerrainType.PLAINS: f"Armed travelers block your path (CR {cr})",
                TerrainType.HILLS: f"Bandits have established a camp here (CR {cr})",
                TerrainType.URBAN: f"Guards patrol this area (CR {cr})",
            },
            EncounterType.UNDEAD: {
                TerrainType.SWAMP: f"Undead creatures rise from the murky waters (CR {cr})",
            },
            EncounterType.DRAGON: {
                TerrainType.MOUNTAIN: f"A dragon's lair dominates this peak (CR {cr})",
            },
        }

        # Try to get specific template
        if encounter_type in templates and terrain_type in templates[encounter_type]:
            return templates[encounter_type][terrain_type]

        # Fallback to generic description
        return f"You encounter {encounter_type.value}s in this {terrain_type.value} (CR {cr})"

    def check_for_encounter_on_travel(
        self,
        from_q: int,
        from_r: int,
        to_q: int,
        to_r: int,
        terrain_type: TerrainType,
        party_level: int = 1
    ) -> Optional[Dict]:
        """
        Check if an encounter occurs when traveling between hexes.
        
        Args:
            from_q, from_r: Starting hex coordinates
            to_q, to_r: Destination hex coordinates
            terrain_type: Terrain of destination hex
            party_level: Average party level
            
        Returns:
            Encounter data if one occurs, None otherwise
        """
        # Verify hexes are adjacent
        distance = self.coord_system.get_distance(from_q, from_r, to_q, to_r)
        if distance != 1:
            raise ValueError("Can only travel to adjacent hexes")

        # Generate encounter at destination
        return self.generate_encounter(to_q, to_r, terrain_type, party_level)
