"""
XP Budget Tables and CR-to-XP Conversion
Based on D&D 2024 official tables
"""

from typing import Dict

# XP budgets per character level and difficulty (for solo player)
XP_BUDGETS: Dict[int, Dict[str, int]] = {
    1: {"low": 50, "moderate": 75, "high": 100},
    2: {"low": 100, "moderate": 150, "high": 200},
    3: {"low": 150, "moderate": 225, "high": 400},
    4: {"low": 250, "moderate": 375, "high": 500},
    5: {"low": 500, "moderate": 750, "high": 1100},
    6: {"low": 600, "moderate": 1000, "high": 1400},
    7: {"low": 750, "moderate": 1300, "high": 1700},
    8: {"low": 900, "moderate": 1600, "high": 2100},
    9: {"low": 1100, "moderate": 1900, "high": 2600},
    10: {"low": 1300, "moderate": 2300, "high": 3100},
    11: {"low": 1600, "moderate": 2700, "high": 3700},
    12: {"low": 1900, "moderate": 3200, "high": 4300},
    13: {"low": 2200, "moderate": 3700, "high": 5000},
    14: {"low": 2600, "moderate": 4300, "high": 5800},
    15: {"low": 3000, "moderate": 5000, "high": 6700},
    16: {"low": 3500, "moderate": 5800, "high": 7800},
    17: {"low": 4000, "moderate": 6700, "high": 9000},
    18: {"low": 4700, "moderate": 7800, "high": 10500},
    19: {"low": 5400, "moderate": 9000, "high": 12100},
    20: {"low": 6300, "moderate": 10500, "high": 14100}
}

# Official D&D 2024 CR to XP conversion table
CR_TO_XP: Dict[str, int] = {
    "0": 10,
    "1/8": 25,
    "1/4": 50,
    "1/2": 100,
    "1": 200,
    "2": 450,
    "3": 700,
    "4": 1100,
    "5": 1800,
    "6": 2300,
    "7": 2900,
    "8": 3900,
    "9": 5000,
    "10": 5900,
    "11": 7200,
    "12": 8400,
    "13": 10000,
    "14": 11500,
    "15": 13000,
    "16": 15000,
    "17": 18000,
    "18": 20000,
    "19": 22000,
    "20": 25000,
    "21": 33000,
    "22": 41000,
    "23": 50000,
    "24": 62000,
    "25": 75000,
    "26": 90000,
    "27": 105000,
    "28": 120000,
    "29": 135000,
    "30": 155000
}


def get_xp_budget(level: int, difficulty: str) -> int:
    """
    Get XP budget for a given level and difficulty.
    
    Args:
        level: Character level (1-20)
        difficulty: 'low', 'moderate', or 'high'
        
    Returns:
        XP budget for encounter
        
    Raises:
        ValueError: If level or difficulty is invalid
    """
    if level not in XP_BUDGETS:
        raise ValueError(f"Invalid level: {level}. Must be 1-20.")
    
    difficulty_lower = difficulty.lower()
    if difficulty_lower not in XP_BUDGETS[level]:
        raise ValueError(f"Invalid difficulty: {difficulty}. Must be 'low', 'moderate', or 'high'.")
    
    return XP_BUDGETS[level][difficulty_lower]


def cr_to_xp(cr: str) -> int:
    """
    Convert Challenge Rating to Experience Points.
    
    Args:
        cr: Challenge rating as string (e.g., "1/4", "5", "10")
        
    Returns:
        XP value for that CR
        
    Examples:
        >>> cr_to_xp("1/4")
        50
        >>> cr_to_xp("5")
        1800
        >>> cr_to_xp("10")
        5900
    """
    if not cr:
        return 10
    
    cr_str = str(cr).strip()
    
    # Direct lookup
    if cr_str in CR_TO_XP:
        return CR_TO_XP[cr_str]
    
    # If not found, try to estimate
    try:
        if '/' in cr_str:
            # Fractional CR
            numerator, denominator = cr_str.split('/')
            cr_float = float(numerator) / float(denominator)
        else:
            cr_float = float(cr_str)
        
        # Estimate XP for unknown CRs
        if cr_float < 1:
            estimated_xp = int(25 + (75 * cr_float))
        else:
            estimated_xp = int(200 * (cr_float ** 1.5))
        
        return max(10, estimated_xp)
    
    except (ValueError, ZeroDivisionError):
        return 10


def get_tier_max_cr(level: int) -> int:
    """
    Get maximum CR for a player level tier.
    
    Args:
        level: Player character level
        
    Returns:
        Maximum CR for encounters at this level
    """
    if level <= 4:
        return 2
    elif level <= 8:
        return 5
    elif level <= 12:
        return 8
    elif level <= 16:
        return 13
    else:
        return 20
