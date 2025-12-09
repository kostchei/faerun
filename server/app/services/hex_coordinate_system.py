"""
Path: server/app/services/hex_coordinate_system.py
Purpose: Hex grid coordinate system utilities for distance and navigation
Logic:
  - Uses axial coordinates (q, r) for hex grid representation
  - Converts to cube coordinates for distance calculation
  - Provides neighbor lookup and direction utilities
  - Based on TaleKeeper's proven hex system implementation
"""

import math
from typing import List, Tuple


class HexCoordinateSystem:
    """
    Utility class for hexagonal grid operations using axial coordinates.
    Supports distance calculation, neighbor finding, and direction mapping.
    """

    # Six directions in axial coordinates (flat-top hexes)
    DIRECTIONS = [
        (1, 0),   # E
        (1, -1),  # NE
        (0, -1),  # NW
        (-1, 0),  # W
        (-1, 1),  # SW
        (0, 1)    # SE
    ]

    DIRECTION_NAMES = ['East', 'Northeast', 'Northwest', 'West', 'Southwest', 'Southeast']

    @staticmethod
    def get_neighbor(q: int, r: int, direction: int) -> Tuple[int, int]:
        """
        Get the coordinates of a neighboring hex in the specified direction.
        
        Args:
            q: Axial q coordinate
            r: Axial r coordinate
            direction: Direction index (0-5)
            
        Returns:
            Tuple of (q, r) for the neighbor
        """
        dq, dr = HexCoordinateSystem.DIRECTIONS[direction % 6]
        return (q + dq, r + dr)

    @staticmethod
    def get_all_neighbors(q: int, r: int) -> List[Tuple[int, int]]:
        """
        Get all 6 neighboring hex coordinates.
        
        Args:
            q: Axial q coordinate
            r: Axial r coordinate
            
        Returns:
            List of (q, r) tuples for all neighbors
        """
        return [
            HexCoordinateSystem.get_neighbor(q, r, i)
            for i in range(6)
        ]

    @staticmethod
    def get_distance(q1: int, r1: int, q2: int, r2: int) -> int:
        """
        Calculate the distance between two hexes in hex grid units.
        Uses cube coordinate conversion for accurate hexagonal distance.
        
        Args:
            q1, r1: First hex coordinates
            q2, r2: Second hex coordinates
            
        Returns:
            Integer distance in hex units
        """
        # Convert axial to cube coordinates and calculate Manhattan distance
        return (abs(q1 - q2) + abs(q1 + r1 - q2 - r2) + abs(r1 - r2)) // 2

    @staticmethod
    def get_direction_index(from_q: int, from_r: int, to_q: int, to_r: int) -> int:
        """
        Get the direction index from one hex to another (for adjacent hexes).
        
        Args:
            from_q, from_r: Starting hex coordinates
            to_q, to_r: Target hex coordinates
            
        Returns:
            Direction index (0-5), or 0 if not adjacent
        """
        dq = to_q - from_q
        dr = to_r - from_r

        for i, (dir_q, dir_r) in enumerate(HexCoordinateSystem.DIRECTIONS):
            if dir_q == dq and dir_r == dr:
                return i

        return 0

    @staticmethod
    def get_direction_name(direction: int) -> str:
        """
        Convert a direction index to a human-readable name.
        
        Args:
            direction: Direction index (0-5)
            
        Returns:
            Direction name (e.g., "East", "Northwest")
        """
        return HexCoordinateSystem.DIRECTION_NAMES[direction % 6]

    @staticmethod
    def get_hexes_in_radius(center_q: int, center_r: int, radius: int) -> List[Tuple[int, int]]:
        """
        Get all hex coordinates within a given radius of a center hex.
        
        Args:
            center_q, center_r: Center hex coordinates
            radius: Radius in hex units
            
        Returns:
            List of (q, r) tuples for all hexes in range
        """
        results = []
        for q in range(center_q - radius, center_q + radius + 1):
            r1 = max(center_r - radius, center_r - q - radius)
            r2 = min(center_r + radius, center_r - q + radius)
            for r in range(r1, r2 + 1):
                results.append((q, r))
        return results
