"""
Path: server/app/routers/combat.py
Purpose: Combat encounter endpoints and WebSocket handler
Logic:
  - POST /start: Initialize new combat with heroes and enemies
  - GET /state: Retrieve current combat state
  - POST /action: Process player actions (move, attack, skill)
  - WS /ws: Real-time combat state updates via WebSocket
  - In-memory CombatState for demo (replace with DB later)
  - ConnectionManager handles WebSocket broadcast to all clients
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

# Import encounter system components
from ..models.encounter import (
    EncounterGenerateRequest,
    TravelRequest,
    TravelResponse,
    TerrainProperties,
    TerrainType,
)
from ..models.region import (
    HexInfo,
    ApplyEventRequest,
    ClearEventRequest
)
from ..services.encounter_service import EncounterService
from ..services.terrain_service import TerrainService
from ..services.hex_coordinate_system import HexCoordinateSystem
from ..services.region_service import RegionService
from ..services.special_hex_service import SpecialHexService
from ..services.event_modifier_service import EventModifierService
from ..services.xp_encounter_generator import XPEncounterGenerator

router = APIRouter()

# Initialize services
DB_PATH = "faerun_hexes.db"
terrain_service = TerrainService()
coord_system = HexCoordinateSystem()
encounter_service = EncounterService(terrain_service, coord_system)

# Initialize region system services
region_service = RegionService(DB_PATH)
special_hex_service = SpecialHexService(DB_PATH)
event_modifier_service = EventModifierService(DB_PATH)

# Initialize XP encounter generator
xp_encounter_gen = XPEncounterGenerator()



class CombatAction(BaseModel):
    action_type: str  # "move", "attack", "skill"
    character_id: str
    target_id: Optional[str] = None
    target_zone: Optional[int] = None


class CombatState(BaseModel):
    round: int = 1
    active_character: str = ""
    characters: list = []
    enemies: list = []


# In-memory combat state for demo
current_combat = CombatState()


@router.post("/start")
async def start_combat():
    """Initialize a new combat encounter."""
    global current_combat
    current_combat = CombatState(
        round=1,
        active_character="hero_1",
        characters=[
            {"id": "hero_1", "name": "Hero", "hp": 50, "zone": 1}
        ],
        enemies=[
            {"id": "enemy_1", "name": "Goblin", "hp": 20, "zone": 2}
        ]
    )
    return {"status": "combat_started", "state": current_combat}


@router.get("/state")
async def get_combat_state():
    """Get current combat state."""
    return current_combat


@router.post("/action")
async def perform_action(action: CombatAction):
    """Process a combat action."""
    # Placeholder logic
    return {
        "status": "action_processed",
        "action": action.model_dump(),
        "result": "hit",
        "damage": 5
    }


# WebSocket for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Echo back with state update
            await manager.broadcast({
                "type": "STATE_UPDATE",
                "state": current_combat.model_dump()
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ===== ENCOUNTER SYSTEM ENDPOINTS =====

@router.post("/encounter/generate")
async def generate_encounter(request: EncounterGenerateRequest):
    """
    Generate an encounter at specified hex coordinates.
    
    Uses deterministic generation based on position seed.
    Encounter probability and CR are based on terrain type and distance.
    """
    # First, determine terrain for this hex
    seed = encounter_service._get_position_seed(request.q, request.r)
    terrain_type = terrain_service.get_random_terrain(seed)
    
    # Generate encounter
    encounter = encounter_service.generate_encounter(
        request.q,
        request.r,
        terrain_type,
        request.party_level
    )
    
    terrain_props = terrain_service.get_terrain_properties(terrain_type)
    
    return {
        "terrain_type": terrain_type.value,
        "terrain_properties": terrain_props,
        "encounter": encounter,
        "message": f"Exploring {terrain_type.value} terrain at ({request.q}, {request.r})"
    }


@router.get("/encounter/terrain/{terrain_type}")
async def get_terrain_info(terrain_type: str):
    """
    Get detailed information about a terrain type.
    
    Returns movement costs, encounter rates, and descriptions.
    """
    try:
        terrain = TerrainType(terrain_type.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid terrain type: {terrain_type}")
    
    props = terrain_service.get_terrain_properties(terrain)
    
    return {
        "terrain_type": terrain.value,
        "properties": props
    }


@router.post("/encounter/travel")
async def travel_to_hex(request: TravelRequest):
    """
    Travel from one hex to an adjacent hex.
    
    Validates adjacency, generates terrain, and checks for encounters.
    """
    # Validate adjacency
    distance = coord_system.get_distance(
        request.from_q, request.from_r,
        request.to_q, request.to_r
    )
    
    if distance != 1:
        raise HTTPException(
            status_code=400,
            detail=f"Can only travel to adjacent hexes. Distance: {distance}"
        )
    
    # Generate terrain for destination
    seed = encounter_service._get_position_seed(request.to_q, request.to_r)
    terrain_type = terrain_service.get_random_terrain(seed)
    
    # Check for encounter
    encounter = encounter_service.check_for_encounter_on_travel(
        request.from_q, request.from_r,
        request.to_q, request.to_r,
        terrain_type,
        request.party_level
    )
    
    # Get terrain properties
    terrain_props = terrain_service.get_terrain_properties(terrain_type)
    
    # Build response message
    direction_idx = coord_system.get_direction_index(
        request.from_q, request.from_r,
        request.to_q, request.to_r
    )
    direction = coord_system.get_direction_name(direction_idx)
    
    if encounter:
        message = f"Traveled {direction} to {terrain_type.value}. {encounter['description']}"
    else:
        message = f"Traveled {direction} to {terrain_type.value}. No encounters."
    
    return TravelResponse(
        success=True,
        terrain_type=terrain_type,
        terrain_properties=terrain_props,
        encounter=encounter,
        distance_traveled=1,
        message=message
    )


# ===== REGIONAL HEX SYSTEM ENDPOINTS =====

@router.get("/hex/info/{q}/{r}")
async def get_hex_info(q: int, r: int):
    """
    Get complete information about a hex including region, special status,  and active events.
    """
    # Get region
    region = region_service.get_region_at_hex(q, r)
    region_info = region_service.get_region_info(region)
    
    # Get terrain (for now, generate randomly)
    seed = encounter_service._get_position_seed(q, r)
    terrain_type = terrain_service.get_random_terrain(seed)
    
    # Check for special location
    special = special_hex_service.get_special_hex(q, r)
    
    # Get active events
    events = event_modifier_service.get_active_events_at_hex(q, r)
    
    # Compute backdrop
    if special:
        backdrop = special['backdrop']
    else:
        backdrop = region_service.get_region_backdrop(region, terrain_type.value)
    
    return {
        "q": q,
        "r": r,
        "region": region_info['name'],
        "base_terrain": terrain_type.value,
        "special_location": special,
        "active_events": events,
        "backdrop": backdrop
    }


@router.get("/map/visible_locations")
async def get_visible_locations():
    """
    Get all cities and dungeons visible on the map.
    """
    return special_hex_service.get_all_visible_locations()


@router.post("/hex/event/apply")
async def apply_event(request: ApplyEventRequest):
    """
    Apply an event modifier to a hex (GM/quest action).
    """
    from ..services.event_modifier_service import EventType
    
    try:
        event_type = EventType(request.event_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid event type: {request.event_type}")
    
    event_id = event_modifier_service.apply_event_modifier(request.q, request.r, event_type)
    
    return {
        "success": True,
        "message": f"Applied {event_type.value} to hex ({request.q}, {request.r})",
        "event_instance_id": event_id
    }


@router.post("/hex/event/clear")
async def clear_event(request: ClearEventRequest):
    """
    Clear an event from a hex (quest completion).
    """
    success = event_modifier_service.clear_event(request.q, request.r, request.event_id)
    
    if success:
        return {
            "success": True,
            "message": f"Cleared event {request.event_id} from hex ({request.q}, {request.r})"
        }
    else:
        raise HTTPException(status_code=404, detail="Event not found")


# ===== XP-BASED ENCOUNTER GENERATION =====

@router.post("/encounter/generate-xp")
async def generate_xp_encounter(
    player_level: int,
    difficulty: str = "moderate"
):
    """
    Generate encounter using XP budget system.
    
    - 10% chance: Legendary (1 powerful creature)
    - 90% chance: Split (2 buckets of boss/minions/mounted)
    
    Args:
        player_level: Character level (1-20)
        difficulty: 'low', 'moderate', or 'high'
    
    Returns:
        XP encounter with pattern, creatures, total XP
    """
    try:
        encounter = xp_encounter_gen.generate_encounter(player_level, difficulty)
        return encounter
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

