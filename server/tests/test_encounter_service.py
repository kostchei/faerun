"""
Path: server/tests/test_encounter_service.py
Purpose: Unit tests for encounter generation
Logic:
  - Tests deterministic encounter generation
  - Tests CR scaling with distance
  - Tests terrain-based encounter rates
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.encounter_service import EncounterService
from app.services.terrain_service import TerrainType


def test_encounter_generation_deterministic():
    """Test that same coordinates generate same encounter with same seed"""
    service = EncounterService()
    
    # Generate encounter at same location multiple times
    encounter1 = service.generate_encounter(5, 5, TerrainType.FOREST, party_level=3)
    encounter2 = service.generate_encounter(5, 5, TerrainType.FOREST, party_level=3)
    
    # Should generate consistently - both None or both same encounter
    if encounter1 is None:
        assert encounter2 is None
    else:
        assert encounter2 is not None
        assert encounter1['seed'] == encounter2['seed']
        assert encounter1['encounter_type'] == encounter2['encounter_type']
    
    print("✓ Deterministic generation test passed")


def test_cr_scaling_with_distance():
    """Test that CR increases with distance from origin"""
    service = EncounterService()
    
    # Near origin
    near_cr = service._calculate_encounter_cr(0, TerrainType.PLAINS, party_level=1)
    
    # Far from origin
    far_cr = service._calculate_encounter_cr(15, TerrainType.PLAINS, party_level=1)
    
    # CR should increase with distance (or be capped by party level)
    assert far_cr >= near_cr
    
    print(f"✓ CR scaling test passed (near: {near_cr}, far: {far_cr})")


def test_terrain_encounter_rates():
    """Test that different terrains have different encounter rates"""
    service = EncounterService()
    
    # Generate many encounters in different terrains
    swamp_encounters = 0
    desert_encounters = 0
    trials = 100
    
    for i in range(trials):
        # Use different coordinates to get different seeds
        swamp_result = service.generate_encounter(i, 0, TerrainType.SWAMP, party_level=1)
        desert_result = service.generate_encounter(i, 100, TerrainType.DESERT, party_level=1)
        
        if swamp_result is not None:
            swamp_encounters += 1
        if desert_result is not None:
            desert_encounters += 1
    
    # Swamp (0.6 rate) should have more encounters than desert (0.2 rate)
    assert swamp_encounters > desert_encounters
    
    print(f"✓ Terrain encounter rate test passed (swamp: {swamp_encounters}/{trials}, desert: {desert_encounters}/{trials})")


def test_terrain_encounter_types():
    """Test that terrain generates appropriate creature types"""
    service = EncounterService()
    
    # Generate encounters in different terrains and check types
    mountain_type = service._get_encounter_type_for_terrain(TerrainType.MOUNTAIN)
    swamp_type = service._get_encounter_type_for_terrain(TerrainType.SWAMP)
    
    # Mountain should have giants or dragons
    assert mountain_type.value in ['giant', 'dragon', 'beast']
    
    # Swamp should have monstrosities, undead, or aberrations
    assert swamp_type.value in ['monstrosity', 'undead', 'aberration']
    
    print("✓ Terrain-specific encounter types test passed")


if __name__ == "__main__":
    test_encounter_generation_deterministic()
    test_cr_scaling_with_distance()
    test_terrain_encounter_rates()
    test_terrain_encounter_types()
    print("\n✅ All encounter service tests passed!")
