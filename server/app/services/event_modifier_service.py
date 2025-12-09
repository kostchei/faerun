"""
Path: server/app/services/event_modifier_service.py
Purpose: Manages event modifiers that temporarily affect hexes
Logic:
  - Tracks active events (Undead Infestation, Demonic Portal, etc.)
  - Applies event-based encounter and backdrop modifications
  - Provides event clearing for quest completion
"""

import sqlite3
import json
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class EventType(str, Enum):
    """Types of event modifiers"""
    UNDEAD_INFESTATION = "undead_infestation"
    DEMONIC_PORTAL = "demonic_portal"
    MARAUDERS = "marauders"
    LEGENDARY_CREATURE = "legendary_creature"


class EventModifierService:
    """
    Service for managing temporary event modifiers on hexes.
    Events override base encounters and modify backdrops/terrain.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_active_events_at_hex(self, q: int, r: int) -> List[Dict]:
        """
        Get all active events at a specific hex.
        
        Args:
            q, r: Hex coordinates
            
        Returns:
            List of active event dicts
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.*, ae.started_at, ae.expires_at
            FROM hex_active_events ae
            JOIN hex_events e ON ae.event_id = e.id
            WHERE ae.q = ? AND ae.r = ? AND ae.is_active = 1
            AND (ae.expires_at IS NULL OR ae.expires_at > datetime('now'))
        ''', (q, r))
        
        rows = cursor.fetchall()
        conn.close()
        
        events = []
        for row in rows:
            events.append({
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'monster_override_chance': row['monster_override_chance'],
                'monster_groups': json.loads(row['monster_groups'] or '[]'),
                'backdrop_modifier': row['backdrop_modifier'],
                'terrain_effect': json.loads(row['terrain_effect'] or '{}'),
                'duration_type': row['duration_type'],
                'started_at': row['started_at'],
                'expires_at': row['expires_at']
            })
        
        return events

    def apply_event_modifier(
        self,
        q: int,
        r: int,
        event_type: EventType,
        expires_at: Optional[str] = None
    ) -> int:
        """
        Apply an event modifier to a hex.
        
        Args:
            q, r: Hex coordinates
            event_type: The type of event to apply
            expires_at: Optional expiration timestamp
            
        Returns:
            Event instance ID
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO hex_active_events (q, r, event_id, expires_at, is_active)
            VALUES (?, ?, ?, ?, 1)
        ''', (q, r, event_type.value, expires_at))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return event_id

    def clear_event(self, q: int, r: int, event_id: str) -> bool:
        """
        Clear an event from a hex (quest completion).
        
        Args:
            q, r: Hex coordinates
            event_id: The event type ID to clear
            
        Returns:
            True if event was cleared
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE hex_active_events
            SET is_active = 0
            WHERE q = ? AND r = ? AND event_id = ? AND is_active = 1
        ''', (q, r, event_id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0

    def clear_all_events_at_hex(self, q: int, r: int) -> int:
        """
        Clear all events from a hex.
        
        Args:
            q, r: Hex coordinates
            
        Returns:
            Number of events cleared
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE hex_active_events
            SET is_active = 0
            WHERE q = ? AND r = ? AND is_active = 1
        ''', (q, r))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected

    def get_event_encounter_override(self, events: List[Dict]) -> Optional[Dict]:
        """
        Get encounter modifications from active events.
        Returns the highest priority event's modifications.
        
        Args:
            events: List of active events from get_active_events_at_hex()
            
        Returns:
            Dict with override_chance and monster_groups, or None
        """
        if not events:
            return None
        
        # Use first event (could implement priority system later)
        event = events[0]
        
        return {
            'override_chance': event['monster_override_chance'],
            'monster_groups': event['monster_groups'],
            'backdrop_modifier': event['backdrop_modifier'],
            'terrain_effect': event['terrain_effect']
        }

    def get_event_info(self, event_type: EventType) -> Dict:
        """
        Get information about an event type.
        
        Args:
            event_type: The event type
            
        Returns:
            Event definition dict
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM hex_events WHERE id = ?
        ''', (event_type.value,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {}
        
        return {
            'id': row['id'],
            'name': row['name'],
            'description': row['description'],
            'monster_override_chance': row['monster_override_chance'],
            'monster_groups': json.loads(row['monster_groups'] or '[]'),
            'backdrop_modifier': row['backdrop_modifier'],
            'terrain_effect': json.loads(row['terrain_effect'] or '{}'),
            'duration_type': row['duration_type']
        }

    def get_all_event_types(self) -> List[Dict]:
        """
        Get all defined event types.
        
        Returns:
            List of event definition dicts
        """
        return [
            self.get_event_info(event_type)
            for event_type in EventType
        ]
