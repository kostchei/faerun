"""Quick test of XP encounter generator"""
from app.services.xp_encounter_generator import XPEncounterGenerator

gen = XPEncounterGenerator()

print("Testing XP Encounter Generator")
print("=" * 50)
print()

# Test Level 5, Moderate
print("Level 5, Moderate (750 XP budget):")
for i in range(5):
    enc = gen.generate_encounter(5, 'moderate')
    print(f"  {i+1}. Pattern: {enc['pattern']:10} | Creatures: {len(enc['creatures'])} | XP: {enc['total_xp']:4}/{enc['budget']}")

print()

# Test Level 1, High
print("Level 1, High (100 XP budget):")
for i in range(3):
    enc = gen.generate_encounter(1, 'high')
    print(f"  {i+1}. Pattern: {enc['pattern']:10} | Creatures: {len(enc['creatures'])} | XP: {enc['total_xp']:4}/{enc['budget']}")

print()

# Test Level 20, High
print("Level 20, High (14100 XP budget):")
for i in range(3):
    enc = gen.generate_encounter(20, 'high')
    print(f"  {i+1}. Pattern: {enc['pattern']:10} | Creatures: {len(enc['creatures'])} | XP: {enc['total_xp']:5}/{enc['budget']}")
    if enc['creatures']:
        print(f"       Creatures: {[c['name'] for c in enc['creatures']]}")
