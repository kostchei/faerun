# Faerun Encounter System Design

## Tiers of Play

Monster selection is organized by character level tiers:

- **Tier 1:** Levels 1-4
- **Tier 2:** Levels 5-8
- **Tier 3:** Levels 9-12
- **Tier 4:** Levels 13-16
- **Tier 5:** Levels 17-20

Each tier has appropriate CR ranges to challenge a solo player.

---

## Encounter Type Distribution

### 10% Legendary Encounters
- Single powerful creature using **100% of XP budget**
- Dramatic boss fights
- Named creatures, dragons, demon lords, etc.

### 90% Split Encounters
Budget divided into **two halves (50% each)**:
- Each half can be: **Boss**, **Minions**, or **Mounts**
- Mounts **cannot appear alone** and **cannot outnumber** the other half

---

## Encounter Patterns

### Valid Combinations

**Note:** Mounted units (rider + mount) count as **1 unit** for gameplay purposes.

| Pattern | Half 1 (50%) | Half 2 (50%) | Total Units |
|---------|--------------|--------------|-------------|
| **Legendary** | - | - | 1 |
| **2 Bosses** | 1 Boss | 1 Boss | 2 |
| **Boss + Minions** | 1 Boss | 4 Minions | 5 |
| **Minions + Boss** | 4 Minions | 1 Boss | 5 |
| **Lots of Minions** | 4 Minions | 4 Minions | 8 |
| **Mounted Boss** | 1 Boss+Mount | - | 1 |
| **Boss + Mounted Minions** | 1 Boss | 4 Mounted | 5 |
| **Mounted Minions** | 4 Mounted | 4 Mounted | 8 |

**Maximum: 8 units on screen at once**

### Rules

1. **Legendary (10% chance):**
   - Use full budget on single creature
   - CR should be challenging for player level

2. **Boss:**
   - Uses ~50% of budget
   - Single powerful creature
   - Can be paired with another boss, minions, or mount

3. **Minions:**
   - 4 creatures of the same type
   - Each worth ~12.5% of budget (50% ÷ 4)
   - Provides tactical variety

4. **Mounts:**
   - Cannot be alone (must have riders)
   - Cannot outnumber the other half
   - Adds mobility and tactics
   - Combined with rider for encounter purposes

---

## XP Budget Examples (Solo Player)

### Tier 1 (Level 1-4)

**Level 1, High Difficulty (100 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 1/2 Orc (100 XP) |
| 2 Bosses | 50 XP | 50 XP | 1× Goblin (50 XP) + 1× Goblin (50 XP) |
| Boss + Minions | 50 XP | 50 XP | 1× Goblin (50 XP) + 4× CR 0 Rats (10 XP = 40 XP) |
| Lots of Minions | 50 XP | 50 XP | 4× Kobolds (25 XP = 100 XP total) |

**Level 4, High Difficulty (500 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 2 (450 XP) - close match |
| 2 Bosses | 250 XP | 250 XP | 1× CR 1 (200 XP) + 1× CR 1 (200 XP) = 400 XP |
| Boss + Minions | 250 XP | 250 XP | 1× CR 1 (200 XP) + 4× Goblins (50 XP = 200 XP) |
| Mounted Boss | 250 XP | 250 XP | 1× CR 1 rider + 1× CR 1 mount (combined) |

---

### Tier 2 (Level 5-8)

**Level 5, Moderate Difficulty (750 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 3 Owlbear (700 XP) |
| 2 Bosses | 375 XP | 375 XP | 1× CR 2 (450 XP) + 1× CR 1 (200 XP) = 650 XP |
| Boss + Minions | 375 XP | 375 XP | 1× CR 2 (450 XP) + 4× Goblins (50 XP = 200 XP) |
| Lots of Minions | 375 XP | 375 XP | 8× Orcs (100 XP = 800 XP) |
| Mounted Minions | 375 XP | 375 XP | 4× Goblin riders (200 XP) + 4× Wolf mounts (200 XP) |

**Level 8, High Difficulty (2,100 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 5 Troll (1,800 XP) |
| 2 Bosses | 1,050 XP | 1,050 XP | 1× CR 4 (1,100 XP) + 1× CR 4 (1,100 XP) |
| Boss + Minions | 1,050 XP | 1,050 XP | 1× CR 4 (1,100 XP) + 4× CR 2 creatures (450 XP = 1,800 XP) |

---

### Tier 3 (Level 9-12)

**Level 10, High Difficulty (3,100 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 8 creature (3,900 XP) |
| 2 Bosses | 1,550 XP | 1,550 XP | 1× CR 5 Troll (1,800 XP) + 1× CR 5 Troll (1,800 XP) |
| Boss + Minions | 1,550 XP | 1,550 XP | 1× CR 5 (1,800 XP) + 4× CR 2 creatures (450 XP = 1,800 XP) |

**Level 12, Moderate Difficulty (3,200 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 8 (3,900 XP) |
| 2 Bosses | 1,600 XP | 1,600 XP | 2× CR 5 Trolls (1,800 XP each = 3,600 XP) |
| Mounted Boss | 1,600 XP | 1,600 XP | 1× CR 5 rider + 1× CR 5 mount |

---

### Tier 4 (Level 13-16)

**Level 15, Moderate Difficulty (5,000 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 9 (5,000 XP) - perfect! |
| 2 Bosses | 2,500 XP | 2,500 XP | 1× CR 7 (2,900 XP) + 1× CR 7 (2,900 XP) |
| Boss + Minions | 2,500 XP | 2,500 XP | 1× CR 7 (2,900 XP) + 4× CR 3 creatures (700 XP = 2,800 XP) |

---

### Tier 5 (Level 17-20)

**Level 20, High Difficulty (14,100 XP):**

| Type | Half 1 | Half 2 | Example |
|------|--------|--------|---------|
| Legendary | - | - | 1× CR 17 Adult Dragon (18,000 XP) |
| 2 Bosses | 7,050 XP | 7,050 XP | 1× CR 11 (7,200 XP) + 1× CR 11 (7,200 XP) |
| Boss + Minions | 7,050 XP | 7,050 XP | 1× CR 11 (7,200 XP) + 4× CR 6 creatures (2,300 XP = 9,200 XP) |

---

## Implementation Algorithm

```python
def generate_encounter(player_level: int, difficulty: str, xp_budget: int):
    # 10% chance for legendary
    if random.random() < 0.1:
        return generate_legendary(xp_budget)
    
    # 90% chance for split encounter
    half_budget = xp_budget // 2
    
    # Choose pattern
    patterns = [
        "two_bosses",
        "boss_minions",
        "minions_boss", 
        "lots_of_minions",
        "mounted_boss",
        "boss_mounted_minions",
        "mounted_minions"
    ]
    
    pattern = random.choice(patterns)
    
    if pattern == "two_bosses":
        boss1 = select_boss(half_budget)
        boss2 = select_boss(half_budget)
        return [boss1, boss2]
    
    elif pattern == "boss_minions":
        boss = select_boss(half_budget)
        minions = select_minions(half_budget, count=4)
        return [boss] + minions
    
    # ... etc
```

---

## Tactical Benefits

1. **Variety:** 8+ different encounter patterns keep combat fresh
2. **Scaling:** Works for all tiers of play (1-20)
3. **Tactical Depth:** 
   - Mounted enemies = mobility
   - Minions = action economy
   - 2 Bosses = dual threats
4. **Side-scroller Friendly:** 2-9 creatures max keeps screen manageable
5. **Solo Balance:** Budget system ensures appropriate challenge

---

## Monster Selection by Tier

**Tier 1 (Levels 1-4):** CR 0 - CR 2
- Rats, Kobolds, Goblins, Orcs, basic beasts

**Tier 2 (Levels 5-8):** CR 1/2 - CR 5
- Orcs, Owlbears, Trolls, basic elementals

**Tier 3 (Levels 9-12):** CR 3 - CR 8
- Trolls, Young Dragons, powerful elementals

**Tier 4 (Levels 13-16):** CR 6 - CR 13
- Adult creatures, powerful demons

**Tier 5 (Levels 17-20):** CR 10 - CR 20+
- Adult Dragons, Demon Lords, Ancient creatures
