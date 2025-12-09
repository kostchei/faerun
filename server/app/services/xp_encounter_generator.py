"""
XP-Based Encounter Generation Service

Generates encounters using D&D 2024 XP budgets:
- 10% Legendary: Full XP budget on 1 creature  
- 90% Split: Two 50% XP buckets spent on boss/minions/mounted
"""

import random
from typing import List, Dict, Any, Optional
from app.data.xp_budgets import get_xp_budget, cr_to_xp, get_tier_max_cr
from app.data.monsters import BASIC_MONSTERS, get_monsters_by_tier, get_mounts, get_riders


class XPEncounterGenerator:
    """
    Generates encounters based on XP budgets with pattern-based design.
    
    Patterns:
    - Legendary (10%): Single creature using full budget
    - Split (90%): Two halves, each can be:
        - Boss: 1 creature (~50% XP)
        - Minions: 4 identical creatures (~12.5% each)
        - Mounted: 1-4 rider+mount pairs
    """
    
    def __init__(self, monster_db: Optional[List[Dict]] = None):
        """
        Initialize encounter generator.
        
        Args:
            monster_db: Monster database. If None, uses BASIC_MONSTERS
        """
        self.monsters = monster_db if monster_db is not None else BASIC_MONSTERS
    
    def generate_encounter(self, player_level: int, difficulty: str = "moderate") -> Dict[str, Any]:
        """
        Generate encounter based on XP budget and player level.
        
        Args:
            player_level: Player character level (1-20)
            difficulty: 'low', 'moderate', or 'high'
            
        Returns:
            Dict with pattern, creatures, total_xp, budget, etc.
        """
        total_xp = get_xp_budget(player_level, difficulty)
        
        # 10% legendary, 90% split
        if random.random() < 0.1:
            return self._generate_legendary(total_xp, player_level, difficulty)
        else:
            return self._generate_split(total_xp, player_level, difficulty)
    
    def _generate_legendary(self, xp: int, level: int, difficulty: str) -> Dict[str, Any]:
        """
        Generate legendary encounter: single creature using full budget.
        
        Args:
            xp: Total XP budget
            level: Player level
            difficulty: Difficulty level
            
        Returns:
            Encounter dict
        """
        creature = self._find_best_creature(xp, level)
        
        if not creature:
            # Fallback to split if no suitable legendary found
            return self._generate_split(xp, level, difficulty)
        
        return {
            "pattern": "legendary",
            "creatures": [creature],
            "total_xp": creature["xp"],
            "budget": xp,
            "player_level": level,
            "difficulty": difficulty,
            "bucket_breakdown": None
        }
    
    def _generate_split(self, total_xp: int, level: int, difficulty: str) -> Dict[str, Any]:
        """
        Generate split encounter: two 50% buckets.
        
        Args:
            total_xp: Total XP budget
            level: Player level
            difficulty: Difficulty level
            
        Returns:
            Encounter dict
        """
        bucket1_xp = total_xp // 2
        bucket2_xp = total_xp // 2
        
        # Spend each bucket
        creatures1, pattern1 = self._spend_bucket(bucket1_xp, level)
        creatures2, pattern2 = self._spend_bucket(bucket2_xp, level)
        
        # Combine
        all_creatures = creatures1 + creatures2
        actual_xp = sum(c.get("xp", 0) for c in all_creatures)
        
        return {
            "pattern": "split",
            "creatures": all_creatures,
            "total_xp": actual_xp,
            "budget": total_xp,
            "player_level": level,
            "difficulty": difficulty,
            "bucket_breakdown": {
                "bucket1": {"pattern": pattern1, "xp": bucket1_xp, "creatures": len(creatures1)},
                "bucket2": {"pattern": pattern2, "xp": bucket2_xp, "creatures": len(creatures2)}
            }
        }
    
    def _spend_bucket(self, xp: int, level: int) -> tuple[List[Dict], str]:
        """
        Spend XP bucket on boss, minions, or mounted units.
        
        Args:
            xp: XP budget for this bucket
            level: Player level
            
        Returns:
            Tuple of (creatures list, pattern name)
        """
        # Random pattern selection
        patterns = ["boss", "minions", "mounted"]
        pattern = random.choice(patterns)
        
        if pattern == "boss":
            creature = self._find_best_creature(xp, level)
            return ([creature] if creature else [], "boss")
        
        elif pattern == "minions":
            return (self._find_4_minions(xp, level), "minions")
        
        elif pattern == "mounted":
            mounted = self._find_mounted_units(xp, level)
            if mounted:
                return (mounted, "mounted")
            # Fallback to minions if no valid mounted units
            return (self._find_4_minions(xp, level), "minions_fallback")
    
    def _find_best_creature(self, xp: int, level: int) -> Optional[Dict]:
        """
        Find single creature closest to XP value.
        
        Args:
            xp: Target XP value
            level: Player level
            
        Returns:
            Monster dict or None
        """
        tier = self._level_to_tier(level)
        tier_max_cr = get_tier_max_cr(level)
        
        # Filter by tier
        valid = [
            m for m in self.monsters 
            if self._cr_to_float(m["cr"]) <= tier_max_cr
        ]
        
        if not valid:
            return None
        
        # Sort by XP descending, find closest without going too far over
        valid_sorted = sorted(valid, key=lambda m: m["xp"], reverse=True)
        
        # Allow up to 20% over budget
        max_xp = int(xp * 1.2)
        
        for monster in valid_sorted:
            if monster["xp"] <= max_xp:
                return monster
        
        # If all too expensive, return cheapest
        return valid_sorted[-1]
    
    def _find_4_minions(self, total_xp: int, level: int) -> List[Dict]:
        """
        Find 4 identical creatures (minions).
        
        Args:
            total_xp: Total XP for all 4 minions
            level: Player level
            
        Returns:
            List of 4 identical monster dicts
        """
        per_creature = total_xp // 4
        creature = self._find_best_creature(per_creature, level)
        
        if not creature:
            return []
        
        return [creature.copy() for _ in range(4)]
    
    def _find_mounted_units(self, total_xp: int, level: int) -> List[Dict]:
        """
        Find mounted units (rider + mount pairs).
        
        Args:
            total_xp: Total XP for mounted units
            level: Player level
            
        Returns:
            List of mounted unit dicts
        """
        # Random number of mounted units (1-4)
        units_count = random.randint(1, 4)
        per_unit = total_xp // units_count
        
        # Split each unit: 60% rider, 40% mount
        rider_xp = int(per_unit * 0.6)
        mount_xp = int(per_unit * 0.4)
        
        # Get tier-appropriate monsters
        tier = self._level_to_tier(level)
        tier_max_cr = get_tier_max_cr(level)
        
        # Find riders and mounts
        valid_riders = [
            m for m in self.monsters
            if m.get("can_ride", False) and self._cr_to_float(m["cr"]) <= tier_max_cr
        ]
        
        valid_mounts = [
            m for m in self.monsters
            if m.get("can_be_mount", False) and self._cr_to_float(m["cr"]) <= tier_max_cr
        ]
        
        if not valid_riders or not valid_mounts:
            return []
        
        # Find closest rider and mount
        rider = min(valid_riders, key=lambda m: abs(m["xp"] - rider_xp))
        mount = min(valid_mounts, key=lambda m: abs(m["xp"] - mount_xp))
        
        # Create mounted units
        mounted_units = []
        for _ in range(units_count):
            mounted_units.append({
                "name": f"{rider['name']} on {mount['name']}",
                "cr": rider["cr"],  # Use rider's CR
                "xp": rider["xp"] + mount["xp"],
                "type": rider["type"],
                "is_mounted": True,
                "rider": rider.copy(),
                "mount": mount.copy()
            })
        
        return mounted_units
    
    def _level_to_tier(self, level: int) -> int:
        """Convert player level to tier of play (1-5)."""
        if level <= 4:
            return 1
        elif level <= 8:
            return 2
        elif level <= 12:
            return 3
        elif level <= 16:
            return 4
        else:
            return 5
    
    def _cr_to_float(self, cr: str) -> float:
        """Convert CR string to float for comparison."""
        try:
            if '/' in cr:
                num, denom = cr.split('/')
                return float(num) / float(denom)
            return float(cr)
        except:
            return 0.0
