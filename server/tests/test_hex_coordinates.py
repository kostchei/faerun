"""
Path: server/tests/test_hex_coordinates.py
Purpose: Unit tests for hex coordinate system
Logic:
  - Tests distance calculations
  - Tests neighbor finding
  - Tests direction utilities
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.hex_coordinate_system import HexCoordinateSystem


def test_distance_calculation():
    """Test hex distance calculation"""
    coord_system = HexCoordinateSystem()
    
    # Same hex
    assert coord_system.get_distance(0, 0, 0, 0) == 0
    
    # Adjacent hexes
    assert coord_system.get_distance(0, 0, 1, 0) == 1
    assert coord_system.get_distance(0, 0, 0, 1) == 1
    
    # Diagonal movement - (0,0) to (3,2) should be 3 hexes
    # Using cube coords: (0,0,-0) to (3,2,-5), Manhattan distance = (3+3+5)/2 = 5.5... wait let me recalculate
    # Actually for (3,2): distance = (|0-3| + |0+0-3-2| + |0-2|) // 2 = (3 + 5 + 2) // 2 = 5
    assert coord_system.get_distance(0, 0, 3, 2) == 5
    
    # Another test
    # (0,0) to (5,5): distance = (|0-5| + |0-5-5| + |0-5|) // 2 = (5 + 10 + 5) // 2 = 10
    assert coord_system.get_distance(0, 0, 5, 5) == 10
    
    print("✓ Distance calculation tests passed")



def test_get_all_neighbors():
    """Test neighbor finding"""
    coord_system = HexCoordinateSystem()
    
    neighbors = coord_system.get_all_neighbors(0, 0)
    
    # Should have 6 neighbors
    assert len(neighbors) == 6
    
    # Each neighbor should be distance 1
    for q, r in neighbors:
        assert coord_system.get_distance(0, 0, q, r) == 1
    
    print("✓ Neighbor finding tests passed")


def test_direction_names():
    """Test direction naming"""
    coord_system = HexCoordinateSystem()
    
    directions = [
        'East', 'Northeast', 'Northwest', 
        'West', 'Southwest', 'Southeast'
    ]
    
    for i, expected_name in enumerate(directions):
        assert coord_system.get_direction_name(i) == expected_name
    
    print("✓ Direction naming tests passed")


def test_hexes_in_radius():
    """Test getting hexes in radius"""
    coord_system = HexCoordinateSystem()
    
    # Radius 0 should only contain center
    hexes_r0 = coord_system.get_hexes_in_radius(0, 0, 0)
    assert len(hexes_r0) == 1
    assert (0, 0) in hexes_r0
    
    # Radius 1 should contain center + 6 neighbors
    hexes_r1 = coord_system.get_hexes_in_radius(0, 0, 1)
    assert len(hexes_r1) == 7
    
    print("✓ Radius tests passed")


if __name__ == "__main__":
    test_distance_calculation()
    test_get_all_neighbors()
    test_direction_names()
    test_hexes_in_radius()
    print("\n✅ All hex coordinate tests passed!")
