"""
Path: server/app/services/special_hex_service.py
Purpose: Manages special fixed hex locations (cities, dungeons)
Logic:
  - Checks if hex is a city or dungeon
  - Returns special encounter rules for these locations
  - Provides list of visible locations for map display
"""

import sqlite3
import json
from typing import Dict, List, Optional


class SpecialHexService:
    """
    Service for managing special fixed locations that override normal encounters.
    Cities have no random encounters. Dungeons have fixed encounter tables.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_special_hex(self, q: int, r: int) -> Optional[Dict]:
        """
        Check if a hex is a special location.
        
        Args:
            q, r: Hex coordinates
            
        Returns:
            Special location dict if exists, None otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM hex_special_locations
            WHERE q = ? AND r = ?
        ''', (q, r))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row['id'],
            'q': row['q'],
            'r': row['r'],
            'type': row['location_type'],
            'name': row['name'],
            'region_id': row['region_id'],
            'monster_groups': json.loads(row['monster_groups'] or '[]'),
            'encounter_types': json.loads(row['encounter_types'] or '[]'),
            'backdrop': row['backdrop_image'],
            'is_visible': bool(row['is_visible'])
        }

    def is_city(self, q: int, r: int) -> bool:
        """Check if hex is a city."""
        special = self.get_special_hex(q, r)
        return special is not None and special['type'] == 'city'

    def is_dungeon(self, q: int, r: int) -> bool:
        """Check if hex is a dungeon."""
        special = self.get_special_hex(q, r)
        return special is not None and special['type'] == 'dungeon'

    def is_visible_on_map(self, q: int, r: int) -> bool:
        """
        Check if hex should be visible on map before discovery.
        Cities and major dungeons are always visible.
        
        Args:
            q, r: Hex coordinates
            
        Returns:
            True if visible on map
        """
        special = self.get_special_hex(q, r)
        return special is not None and special.get('is_visible', False)

    def get_all_visible_locations(self) -> List[Dict]:
        """
        Get all cities and dungeons that are visible on the map.
        Used for map rendering.
        
        Returns:
            List of special location dicts
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM hex_special_locations
            WHERE is_visible = 1
            ORDER BY name
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        locations = []
        for row in rows:
            locations.append({
                'id': row['id'],
                'q': row['q'],
                'r': row['r'],
                'type': row['location_type'],
                'name': row['name'],
                'backdrop': row['backdrop_image'],
                'region_id': row['region_id']
            })
        
        return locations

    def add_special_location(
        self,
        q: int,
        r: int,
        location_type: str,
        name: str,
        region_id: str,
        backdrop: str,
        is_visible: bool = True
    ) -> str:
        """
        Add a new special location (GM tool).
        
        Args:
            q, r: Hex coordinates
            location_type: 'city' or 'dungeon'
            name: Location name
            region_id: Parent region
            backdrop: Backdrop image filename
            is_visible: Whether visible on map
            
        Returns:
            Location ID
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        location_id = name.lower().replace(' ', '_')
        
        cursor.execute('''
            INSERT OR REPLACE INTO hex_special_locations
            (id, q, r, location_type, name, region_id, monster_groups, encounter_types, backdrop_image, is_visible)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (location_id, q, r, location_type, name, region_id, '[]', '[]', backdrop, is_visible))
        
        conn.commit()
        conn.close()
        
        return location_id
