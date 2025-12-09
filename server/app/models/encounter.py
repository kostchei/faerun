"""
Path: server/app/models/encounter.py
Purpose: Pydantic models for encounter system
Logic:
  - Defines data models for encounters, terrain, and hex locations
  - Provides validation and serialization for API responses
  - Ensures type safety across the encounter system
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class TerrainType(str, Enum):
    """Available terrain types"""
    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    HILLS = "hills"
    SWAMP = "swamp"
    DESERT = "desert"
    URBAN = "urban"


class EncounterType(str, Enum):
    """Types of encounters"""
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


class HexLocation(BaseModel):
    """Represents a hex grid location with terrain information"""
    q: int = Field(..., description="Axial Q coordinate")
    r: int = Field(..., description="Axial R coordinate")
    terrain_type: TerrainType = Field(..., description="Type of terrain at this location")
    distance_from_origin: int = Field(default=0, description="Distance from (0,0) in hex units")


class TerrainProperties(BaseModel):
    """Properties and statistics for a terrain type"""
    terrain_type: TerrainType
    move_cost: float = Field(..., description="Movement cost multiplier")
    encounter_rate: float = Field(..., description="Base encounter probability (0.0-1.0)")
    visibility: str = Field(..., description="Visibility level (low/medium/high)")
    description: str = Field(..., description="Narrative description")
    navigation_dc: int = Field(..., description="DC for navigation/survival checks")


class EncounterData(BaseModel):
    """Complete encounter information"""
    q: int = Field(..., description="Hex Q coordinate")
    r: int = Field(..., description="Hex R coordinate")
    terrain_type: str = Field(..., description="Terrain where encounter occurs")
    encounter_type: str = Field(..., description="Type of creatures encountered")
    cr: int = Field(..., description="Challenge Rating")
    description: str = Field(..., description="Narrative description of the encounter")
    distance_from_origin: int = Field(..., description="Distance from starting point")
    encounter_distance_ft: int = Field(..., description="Starting distance to encounter in feet (visibility-based)")
    seed: int = Field(..., description="Random seed used for generation")



class EncounterGenerateRequest(BaseModel):
    """Request to generate an encounter"""
    q: int = Field(..., description="Hex Q coordinate")
    r: int = Field(..., description="Hex R coordinate")
    party_level: int = Field(default=1, ge=1, le=20, description="Average party level")


class TravelRequest(BaseModel):
    """Request to travel between hexes"""
    from_q: int = Field(..., description="Starting Q coordinate")
    from_r: int = Field(..., description="Starting R coordinate")
    to_q: int = Field(..., description="Destination Q coordinate")
    to_r: int = Field(..., description="Destination R coordinate")
    party_level: int = Field(default=1, ge=1, le=20, description="Average party level")


class TravelResponse(BaseModel):
    """Response from travel action"""
    success: bool = Field(..., description="Whether travel was successful")
    terrain_type: TerrainType = Field(..., description="Terrain at destination")
    terrain_properties: Dict = Field(..., description="Properties of the terrain")
    encounter: Optional[Dict] = Field(None, description="Encounter if one occurred")
    distance_traveled: int = Field(..., description="Hexes traveled")
    message: str = Field(..., description="Narrative message")


# ===== XP-BASED ENCOUNTER MODELS =====

class MountedUnit(BaseModel):
    """A rider + mount combined unit"""
    rider: Dict = Field(..., description="Rider creature data")
    mount: Dict = Field(..., description="Mount creature data")
    combined_xp: int = Field(..., description="Total XP of rider + mount")


class CreatureInEncounter(BaseModel):
    """Creature in an XP-based encounter"""
    name: str = Field(..., description="Creature name")
    cr: str = Field(..., description="Challenge Rating")
    xp: int = Field(..., description="Experience points")
    type: str = Field(..., description="Creature type (humanoid, beast, etc.)")
    is_mounted: bool = Field(default=False, description="Whether this is a mounted unit")
    mount_data: Optional[Dict] = Field(None, description="Mount data if mounted")


class XPEncounter(BaseModel):
    """XP budget-based encounter result"""
    pattern: str = Field(..., description="Encounter pattern: 'legendary' or 'split'")
    creatures: List[Dict] = Field(..., description="List of creatures in encounter")
    total_xp: int = Field(..., description="Actual total XP of encounter")
    budget: int = Field(..., description="Target XP budget")
    player_level: int = Field(..., description="Player character level")
    difficulty: str = Field(..., description="Encounter difficulty")
    bucket_breakdown: Optional[Dict] = Field(None, description="How XP was split between buckets")


class XPEncounterRequest(BaseModel):
    """Request to generate XP-based encounter"""
    player_level: int = Field(..., ge=1, le=20, description="Player level (1-20)")
    difficulty: str = Field(default="moderate", description="'low', 'moderate', or 'high'")
