"""
Path: server/app/services/region_service.py
Purpose: Regional zone management for Faerun hex map
Logic:
  - Manages 4 regional zones (Countryside, Icewind, Moonshae, Calimshan)
  - Provides region-specific monster groups and terrain types
  - Generates backdrops based on region + terrain combinations
"""

import sqlite3
import json
from typing import Dict, List, Optional
from enum import Enum


class RegionType(str, Enum):
    """4 regional zones in Faerun"""
    COUNTRYSIDE = "countryside"
    ICEWIND = "icewind"
    MOONSHAE = "moonshae"
    CALIMSHAN = "calimshan"


class RegionService:
    """
    Service for managing regional zones and their properties.
    Each region has unique monster groups, terrain types, and visual backdrops.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_region_at_hex(self, q: int, r: int) -> RegionType:
        """
        Get the region for specific hex coordinates.
        
        Args:
            q, r: Hex coordinates
            
        Returns:
            RegionType enum value
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT region_id FROM hex_grid
            WHERE q = ? AND r = ?
        ''', (q, r))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return RegionType(row['region_id'])
        
        # Default fallback: assign based on simple coordinate rules
        # This is a placeholder - ideally all hexes would be pre-mapped
        return self._assign_default_region(q, r)

    def _assign_default_region(self, q: int, r: int) -> RegionType:
        """
        Assign a default region based on coordinate heuristics.
        This is a fallback for unmapped hexes.
        
        Args:
            q, r: Hex coordinates
            
        Returns:
            RegionType
        """
        # Simple heuristic: north = icewind, south = calimshan, etc.
        # TODO: Replace with actual map-based assignment
        if r < -10:  # Far north
            return RegionType.ICEWIND
        elif r > 10:  # Far south
            return RegionType.CALIMSHAN
        elif q < -10:  # Far west
            return RegionType.MOONSHAE
        else:  # Central/default
            return RegionType.COUNTRYSIDE

    def get_region_info(self, region: RegionType) -> Dict:
        """
        Get complete information about a region.
        
        Args:
            region: The region type
            
        Returns:
            Dict with region name, description, monster groups, terrain types
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM hex_regions WHERE id = ?
        ''', (region.value,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {}
        
        return {
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'terrain_types': json.loads(row['default_terrain_types'] or '[]'),
            'monster_groups': json.loads(row['monster_groups'] or '[]'),
            'backdrop_prefix': row['backdrop_prefix']
        }

    def get_region_monster_groups(self, region: RegionType) -> List[str]:
        """
        Get the list of monster groups for a region.
        
        Args:
            region: The region type
            
        Returns:
            List of monster group names (e.g., ['beast', 'humanoid'])
        """
        info = self.get_region_info(region)
        return info.get('monster_groups', [])

    def get_region_terrain_types(self, region: RegionType) -> List[str]:
        """
        Get the list of terrain types common in a region.
        
        Args:
            region: The region type
            
        Returns:
            List of terrain type names
        """
        info = self.get_region_info(region)
        return info.get('terrain_types', [])

    def get_region_backdrop(self, region: RegionType, terrain: str) -> str:
        """
        Get the backdrop image path for a region + terrain combination.
        
        Args:
            region: The region type
            terrain: The terrain type (e.g., 'forest', 'desert')
            
        Returns:
            Backdrop image path (e.g., 'countryside_forest.jpg')
        """
        info = self.get_region_info(region)
        prefix = info.get('backdrop_prefix', 'default')
        return f"{prefix}_{terrain}.jpg"

    def set_hex_region(self, q: int, r: int, region: RegionType, terrain: Optional[str] = None):
        """
        Assign a region to a specific hex (used for map setup).
        
        Args:
            q, r: Hex coordinates
            region: The region to assign
            terrain: Optional terrain type override
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO hex_grid (q, r, region_id, base_terrain, discovered)
            VALUES (?, ?, ?, ?, 0)
        ''', (q, r, region.value, terrain))
        
        conn.commit()
        conn.close()

    def get_all_regions(self) -> List[Dict]:
        """
        Get information about all regions.
        
        Returns:
            List of region info dicts
        """
        return [
            self.get_region_info(region)
            for region in RegionType
        ]
