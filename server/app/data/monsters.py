"""
Basic monster dataset for encounter generation
Includes XP values, CR, type, and mount/rider capabilities
"""

from typing import List, Dict, Any

# Basic monster set for testing and initial implementation
BASIC_MONSTERS: List[Dict[str, Any]] = [
    # Tier 1 (Levels 1-4): CR 0 - 2
    {"name": "Rat", "cr": "0", "xp": 10, "type": "beast", "can_be_mount": False, "can_ride": False},
    {"name": "Kobold", "cr": "1/8", "xp": 25, "type": "humanoid", "can_be_mount": False, "can_ride": True},
    {"name": "Goblin", "cr": "1/4", "xp": 50, "type": "humanoid", "can_be_mount": False, "can_ride": True},
    {"name": "Wolf", "cr": "1/4", "xp": 50, "type": "beast", "can_be_mount": True, "can_ride": False},
    {"name": "Skeleton", "cr": "1/4", "xp": 50, "type": "undead", "can_be_mount": False, "can_ride": False},
    {"name": "Zombie", "cr": "1/4", "xp": 50, "type": "undead", "can_be_mount": False, "can_ride": False},
    {"name": "Orc", "cr": "1/2", "xp": 100, "type": "humanoid", "can_be_mount": False, "can_ride": True},
    {"name": "Warg", "cr": "1/2", "xp": 100, "type": "beast", "can_be_mount": True, "can_ride": False},
    {"name": "Wight", "cr": "3", "xp": 700, "type": "undead", "can_be_mount": False, "can_ride": False},
    {"name": "Ghoul", "cr": "1", "xp": 200, "type": "undead", "can_be_mount": False, "can_ride": False},
    {"name": "Hobgoblin", "cr": "1/2", "xp": 100, "type": "humanoid", "can_be_mount": False, "can_ride": True},
    {"name": "Bugbear", "cr": "1", "xp": 200, "type": "humanoid", "can_be_mount": False, "can_ride": False},
    
    # Tier 2 (Levels 5-8): CR 1/2 - 5
    {"name": "Ogre", "cr": "2", "xp": 450, "type": "giant", "can_be_mount": False, "can_ride": False},
    {"name": "Owlbear", "cr": "3", "xp": 700, "type": "monstrosity", "can_be_mount": False, "can_ride": False},
    {"name": "Manticore", "cr": "3", "xp": 700, "type": "monstrosity", "can_be_mount": False, "can_ride": False},
    {"name": "Troll", "cr": "5", "xp": 1800, "type": "giant", "can_be_mount": False, "can_ride": False},
    {"name": "Dire Wolf", "cr": "1", "xp": 200, "type": "beast", "can_be_mount": True, "can_ride": False},
    {"name": "Wyvern", "cr": "6", "xp": 2300, "type": "dragon", "can_be_mount": True, "can_ride": False},
    {"name": "Hill Giant", "cr": "5", "xp": 1800, "type": "giant", "can_be_mount": False, "can_ride": False},
    
    # Tier 3 (Levels 9-12): CR 3 - 8
    {"name": "Young Black Dragon", "cr": "7", "xp": 2900, "type": "dragon", "can_be_mount": False, "can_ride": False},
    {"name": "Young Green Dragon", "cr": "8", "xp": 3900, "type": "dragon", "can_be_mount": False, "can_ride": False},
    {"name": "Stone Giant", "cr": "7", "xp": 2900, "type": "giant", "can_be_mount": False, "can_ride": False},
    {"name": "Fire Giant", "cr": "9", "xp": 5000, "type": "giant", "can_be_mount": False, "can_ride": False},
    {"name": "Wraith", "cr": "5", "xp": 1800, "type": "undead", "can_be_mount": False, "can_ride": False},
    
    # Tier 4 (Levels 13-16): CR 6 - 13
    {"name": "Young Red Dragon", "cr": "10", "xp": 5900, "type": "dragon", "can_be_mount": False, "can_ride": False},
    {"name": "Adult Black Dragon", "cr": "14", "xp": 11500, "type": "dragon", "can_be_mount": False, "can_ride": False},
    {"name": "Frost Giant", "cr": "8", "xp": 3900, "type": "giant", "can_be_mount": False, "can_ride": False},
    {"name": "Cloud Giant", "cr": "9", "xp": 5000, "type": "giant", "can_be_mount": False, "can_ride": False},
    {"name": "Vampire", "cr": "13", "xp": 10000, "type": "undead", "can_be_mount": False, "can_ride": False},
    
    # Tier 5 (Levels 17-20): CR 10 - 20+
    {"name": "Adult Red Dragon", "cr": "17", "xp": 18000, "type": "dragon", "can_be_mount": False, "can_ride": False},
    {"name": "Ancient Black Dragon", "cr": "21", "xp": 33000, "type": "dragon", "can_be_mount": False, "can_ride": False},
    {"name": "Ancient Red Dragon", "cr": "24", "xp": 62000, "type": "dragon", "can_be_mount": False, "can_ride": False},
    {"name": "Lich", "cr": "21", "xp": 33000, "type": "undead", "can_be_mount": False, "can_ride": False},
    {"name": "Tarrasque", "cr": "30", "xp": 155000, "type": "monstrosity", "can_be_mount": False, "can_ride": False},
]


def get_monsters_by_tier(tier: int) -> List[Dict[str, Any]]:
    """
    Get monsters appropriate for a tier of play.
    
    Args:
        tier: 1 (levels 1-4), 2 (5-8), 3 (9-12), 4 (13-16), or 5 (17-20)
        
    Returns:
        List of monster dicts for that tier
    """
    cr_ranges = {
        1: (0, 2),      # CR 0 - 2
        2: (0.5, 5),    # CR 1/2 - 5
        3: (3, 8),      # CR 3 - 8
        4: (6, 13),     # CR 6 - 13
        5: (10, 30)     # CR 10 - 30
    }
    
    if tier not in cr_ranges:
        tier = 1
    
    min_cr, max_cr = cr_ranges[tier]
    
    # Convert CR strings to floats for comparison
    def cr_to_float(cr_str: str) -> float:
        try:
            if '/' in cr_str:
                num, denom = cr_str.split('/')
                return float(num) / float(denom)
            return float(cr_str)
        except:
            return 0.0
    
    return [
        m for m in BASIC_MONSTERS 
        if min_cr <= cr_to_float(m["cr"]) <= max_cr
    ]


def get_mounts() -> List[Dict[str, Any]]:
    """Get all creatures that can be mounts."""
    return [m for m in BASIC_MONSTERS if m.get("can_be_mount", False)]


def get_riders() -> List[Dict[str, Any]]:
    """Get all creatures that can ride mounts."""
    return [m for m in BASIC_MONSTERS if m.get("can_ride", False)]
