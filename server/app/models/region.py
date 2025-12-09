"""
Path: server/app/models/region.py
Purpose: Pydantic models for regional hex system
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RegionInfo(BaseModel):
    """Information about a regional zone"""
    name: str = Field(..., description="Region name (e.g., 'Countryside')")
    description: str = Field(..., description="Region description")
    monster_groups: List[str] = Field(..., description="List of monster types in region")
    terrain_types: List[str] = Field(..., description="Common terrain types in region")
    backdrop_prefix: str = Field(..., description="Prefix for backdrop images")


class SpecialHexLocation(BaseModel):
    """Special fixed location (city or dungeon)"""
    q: int = Field(..., description="Hex Q coordinate")
    r: int = Field(..., description="Hex R coordinate")
    location_type: str = Field(..., description="'city' or 'dungeon'")
    name: str = Field(..., description="Location name (e.g., 'Waterdeep')")
    region_id: str = Field(..., description="Parent region ID")
    is_visible: bool = Field(default=True, description="Visible on map before discovery")
    backdrop: str = Field(..., description="Backdrop image filename")


class EventModifier(BaseModel):
    """Event modifier affecting a hex"""
    id: str = Field(..., description="Event type ID")
    name: str = Field(..., description="Event name (e.g., 'Undead Infestation')")
    description: str = Field(..., description="Event description")
    monster_override_chance: float = Field(..., description="Probability of encounter override (0.0-1.0)")
    monster_groups: List[str] = Field(..., description="Monster types for this event")
    backdrop_modifier: str = Field(..., description="Backdrop modification (e.g., 'fog', 'red_sky')")
    terrain_effect: Dict[str, Any] = Field(default_factory=dict, description="Terrain modifications")


class HexInfo(BaseModel):
    """Complete information about a hex"""
    q: int = Field(..., description="Hex Q coordinate")
    r: int = Field(..., description="Hex R coordinate")
    region: str = Field(..., description="Base region name")
    base_terrain: str = Field(..., description="Terrain type at hex")
    special_location: Optional[SpecialHexLocation] = Field(None, description="Special location if present")
    active_events: List[EventModifier] = Field(default_factory=list, description="Active events at hex")
    backdrop: str = Field(..., description="Computed backdrop image path")


class ApplyEventRequest(BaseModel):
    """Request to apply event to hex"""
    q: int = Field(..., description="Hex Q coordinate")
    r: int = Field(..., description="Hex R coordinate")
    event_type: str = Field(..., description="Event type ID to apply")


class ClearEventRequest(BaseModel):
    """Request to clear event from hex"""
    q: int = Field(..., description="Hex Q coordinate")
    r: int = Field(..., description="Hex R coordinate")
    event_id: str = Field(..., description="Event type ID to clear")
