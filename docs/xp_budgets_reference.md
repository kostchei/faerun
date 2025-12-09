# D&D 2024 Experience Points Reference

## CR to XP Conversion

From TaleKeeper's `cr_to_xp.py` (Official D&D 2024 tables):

| CR | XP | Common Example |
|----|-----|----------------|
| 0 | 10 | Rat |
| 1/8 | 25 | Kobold |
| 1/4 | 50 | Goblin |
| 1/2 | 100 | Orc |
| 1 | 200 | - |
| 2 | 450 | - |
| 3 | 700 | Owlbear |
| 4 | 1,100 | - |
| 5 | 1,800 | Troll |
| 6 | 2,300 | - |
| 7 | 2,900 | - |
| 8 | 3,900 | - |
| 9 | 5,000 | - |
| 10 | 5,900 | Young Dragon |
| 11 | 7,200 | - |
| 12 | 8,400 | - |
| 13 | 10,000 | - |
| 14 | 11,500 | - |
| 15 | 13,000 | - |
| 16 | 15,000 | - |
| 17 | 18,000 | Adult Dragon |
| 18 | 20,000 | - |
| 19 | 22,000 | - |
| 20 | 25,000 | - |
| 21 | 33,000 | - |
| 22 | 41,000 | - |
| 23 | 50,000 | - |
| 24 | 62,000 | Ancient Dragon |
| 30 | 155,000 | Tarrasque |

---

## XP Budget Per Encounter (By Level & Difficulty)

From TaleKeeper's `encounter_generator.py` - for **single party member**:

| Level | Low Difficulty | Moderate Difficulty | High Difficulty |
|-------|---------------|---------------------|-----------------|
| 1 | 50 | 75 | 100 |
| 2 | 100 | 150 | 200 |
| 3 | 150 | 225 | 400 |
| 4 | 250 | 375 | 500 |
| 5 | 500 | 750 | 1,100 |
| 6 | 600 | 1,000 | 1,400 |
| 7 | 750 | 1,300 | 1,700 |
| 8 | 900 | 1,600 | 2,100 |
| 9 | 1,100 | 1,900 | 2,600 |
| 10 | 1,300 | 2,300 | 3,100 |
| 11 | 1,600 | 2,700 | 3,700 |
| 12 | 1,900 | 3,200 | 4,300 |
| 13 | 2,200 | 3,700 | 5,000 |
| 14 | 2,600 | 4,300 | 5,800 |
| 15 | 3,000 | 5,000 | 6,700 |
| 16 | 3,500 | 5,800 | 7,800 |
| 17 | 4,000 | 6,700 | 9,000 |
| 18 | 4,700 | 7,800 | 10,500 |
| 19 | 5,400 | 9,000 | 12,100 |
| 20 | 6,300 | 10,500 | 14,100 |

**IMPORTANT:** These budgets are **per character**, not for the entire party!

For a **4-person party**:
- Level 1 High difficulty = 100 × 4 = **400 XP** total
- Level 5 Moderate difficulty = 750 × 4 = **3,000 XP** total
- Level 10 High difficulty = 3,100 × 4 = **12,400 XP** total

---

## Encounter Examples

### Level 1 Party (4 characters), High Difficulty
- **Budget:** 400 XP
- **Options:**
  - 8× Goblins (CR 1/4 = 50 XP each = 400 XP total)
  - 2× Orcs (CR 1/2 = 100 XP each = 200 XP) + 4× Goblins (50 XP = 200 XP) = 400 XP
  - 2× CR 1 creatures (200 XP each = 400 XP)

### Level 5 Party (4 characters), Moderate Difficulty
- **Budget:** 3,000 XP
- **Options:**
  - 1× Troll (CR 5 = 1,800 XP) + 1× CR 3 creature (700 XP) + 1× CR 1/2 (100 XP) ≈ 2,600 XP
  - 2× CR 4 creatures (1,100 XP each = 2,200 XP) + 2× CR 2 creatures (450 XP each = 900 XP) = 3,100 XP

### Level 10 Party (4 characters), High Difficulty
- **Budget:** 12,400 XP
- **Options:**
  - 2× Young Dragons (CR 10 = 5,900 XP each = 11,800 XP)
  - 1× CR 13 (10,000 XP) + 1× CR 5 (1,800 XP) = 11,800 XP

---

## TaleKeeper Encounter Patterns

TaleKeeper uses different patterns based on difficulty:

### High Difficulty Patterns
1. **Solo**: Single strongest monster
2. **Pair**: 2 different monster types
3. **Leader + Minions**: 1 leader + 1-4 minions of same type

### Low/Moderate Difficulty Patterns
1. **Pair**: 2 different monster types
2. **Leader + Minions**: 1 leader + 1-4 minions of same type

**Beast Pairing Rule:** If one monster is a beast, the other must be either:
- Another beast, OR
- A creature with Intelligence 6+

---

## XP Rewards for Non-Combat

**Parlay (Negotiation):**
- 50% of total encounter XP

**Encounter Avoidance (Stealth/Trickery):**
- 33% of total encounter XP

---

## For Faerun Implementation

**Recommended approach:**
1. Store this XP budget table in database or config
2. Use party size and average party level to calculate budget
3. Generate encounters that fit within budget
4. Track XP per monster using CR_TO_XP table

**Example calculation:**
```python
def calculate_encounter_budget(party_size: int, party_level: int, difficulty: str) -> int:
    \"\"\"Calculate total XP budget for encounter\"\"\"
    per_character_budget = XP_BUDGETS[party_level][difficulty]
    return per_character_budget * party_size
```
