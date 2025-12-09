"""
Path: server/app/services/terrain_service.py
Purpose: Terrain type definitions and property management
Logic:
  - Defines terrain types with movement costs and encounter rates
  - Provides terrain generation and property lookup
  - Calculates skill DCs for terrain navigation
  - Based on TaleKeeper's biome system
"""

import random
from typing import Dict, Optional
from enum import Enum


class TerrainType(str, Enum):
    """Enumeration of available terrain types"""
    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    HILLS = "hills"
    SWAMP = "swamp"
    DESERT = "desert"
    URBAN = "urban"


class TerrainService:
    """
    Service for managing terrain properties and generation.
    Provides terrain stats, random generation, and navigation difficulty.
    """

    # Terrain properties based on TaleKeeper's system
    TERRAIN_PROPERTIES = {
        TerrainType.PLAINS: {
            'move_cost': 1.0,
            'encounter_rate': 0.3,
            'visibility': 'high',
            'description': 'Open grasslands with good visibility',
            'navigation_dc': 10,
        },
        TerrainType.FOREST: {
            'move_cost': 1.2,
            'encounter_rate': 0.5,
            'visibility': 'low',
            'description': 'Dense woodland with limited sightlines',
            'navigation_dc': 12,
        },
        TerrainType.MOUNTAIN: {
            'move_cost': 1.5,
            'encounter_rate': 0.4,
            'visibility': 'high',
            'description': 'Rocky terrain with steep inclines',
            'navigation_dc': 15,
        },
        TerrainType.HILLS: {
            'move_cost': 1.2,
            'encounter_rate': 0.35,
            'visibility': 'medium',
            'description': 'Rolling terrain with moderate elevation changes',
            'navigation_dc': 12,
        },
        TerrainType.SWAMP: {
            'move_cost': 1.5,
            'encounter_rate': 0.6,
            'visibility': 'low',
            'description': 'Waterlogged ground with thick vegetation',
            'navigation_dc': 14,
        },
        TerrainType.DESERT: {
            'move_cost': 1.3,
            'encounter_rate': 0.2,
            'visibility': 'high',
            'description': 'Arid terrain with sparse vegetation',
            'navigation_dc': 13,
        },
        TerrainType.URBAN: {
            'move_cost': 1.0,
            'encounter_rate': 0.4,
            'visibility': 'medium',
            'description': 'Settled area with buildings and roads',
            'navigation_dc': 8,
        },
    }

    @staticmethod
    def get_terrain_properties(terrain_type: TerrainType) -> Dict:
        """
        Get the properties for a specific terrain type.
        
        Args:
            terrain_type: The terrain type to query
            
        Returns:
            Dictionary of terrain properties
        """
        return TerrainService.TERRAIN_PROPERTIES.get(terrain_type, {})

    @staticmethod
    def get_random_terrain(seed: int) -> TerrainType:
        """
        Generate a random terrain type based on a seed.
        Uses deterministic random generation for consistency.
        
        Args:
            seed: Random seed for generation
            
        Returns:
            A TerrainType value
        """
        random.seed(seed)
        # Exclude urban from random generation (should be placed manually)
        terrain_choices = [
            TerrainType.PLAINS,
            TerrainType.FOREST,
            TerrainType.MOUNTAIN,
            TerrainType.HILLS,
            TerrainType.SWAMP,
            TerrainType.DESERT,
        ]
        return random.choice(terrain_choices)

    @staticmethod
    def get_terrain_dc(terrain_type: TerrainType) -> int:
        """
        Get the navigation/survival DC for a terrain type.
        
        Args:
            terrain_type: The terrain type
            
        Returns:
            DC value for skill checks
        """
        props = TerrainService.get_terrain_properties(terrain_type)
        return props.get('navigation_dc', 12)

    @staticmethod
    def get_move_cost(terrain_type: TerrainType) -> float:
        """
        Get the movement cost multiplier for a terrain type.
        
        Args:
            terrain_type: The terrain type
            
        Returns:
            Movement cost multiplier (1.0 = normal)
        """
        props = TerrainService.get_terrain_properties(terrain_type)
        return props.get('move_cost', 1.0)

    @staticmethod
    def get_encounter_rate(terrain_type: TerrainType) -> float:
        """
        Get the base encounter rate for a terrain type.
        
        Args:
            terrain_type: The terrain type
            
        Returns:
            Encounter probability (0.0 - 1.0)
        """
        props = TerrainService.get_terrain_properties(terrain_type)
        return props.get('encounter_rate', 0.3)

    @staticmethod
    def calculate_encounter_distance(terrain_type: TerrainType) -> int:
        """
        Calculate encounter starting distance based on terrain visibility.
        Uses dice formulas from dnd-encounters-24 app.
        
        Distance represents how far away the party spots the encounter,
        influenced by terrain visibility and line of sight.
        
        Args:
            terrain_type: The terrain type
            
        Returns:
            Distance in feet (rolled randomly based on terrain)
        """
        # Terrain-based distance formulas (from dnd-encounters-24)
        distance_formulas = {
            TerrainType.PLAINS: (6, 6, 10),      # 6d6 * 10 ft (avg 210 ft, range 60-360)
            TerrainType.FOREST: (2, 8, 10),      # 2d8 * 10 ft (avg 90 ft, range 20-160)
            TerrainType.MOUNTAIN: (4, 10, 10),   # 4d10 * 10 ft (avg 220 ft, range 40-400)
            TerrainType.HILLS: (2, 10, 10),      # 2d10 * 10 ft (avg 110 ft, range 20-200)
            TerrainType.SWAMP: (2, 6, 10),       # 2d6 * 10 ft (avg 70 ft, range 20-120)
            TerrainType.DESERT: (6, 6, 10),      # 6d6 * 10 ft (avg 210 ft, range 60-360)
            TerrainType.URBAN: (2, 10, 10),      # 2d10 * 10 ft (avg 110 ft, range 20-200)
        }
        
        formula = distance_formulas.get(terrain_type, (2, 6, 10))
        num_dice, die_size, multiplier = formula
        
        # Roll dice and calculate distance
        total = sum(random.randint(1, die_size) for _ in range(num_dice))
        return total * multiplier

    @staticmethod
    def get_average_encounter_distance(terrain_type: TerrainType) -> int:
        """
        Get the average encounter distance for a terrain type (for display/info).
        
        Args:
            terrain_type: The terrain type
            
        Returns:
            Average distance in feet
        """
        averages = {
            TerrainType.PLAINS: 210,
            TerrainType.FOREST: 90,
            TerrainType.MOUNTAIN: 220,
            TerrainType.HILLS: 110,
            TerrainType.SWAMP: 70,
            TerrainType.DESERT: 210,
            TerrainType.URBAN: 110,
        }
        return averages.get(terrain_type, 100)

