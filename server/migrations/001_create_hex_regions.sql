-- Faerun Region System Database Schema
-- Creates tables for regional zones, special hexes, and event modifiers

-- Region definitions (4 zones: Countryside, Icewind, Moonshae, Calimshan)
CREATE TABLE IF NOT EXISTS hex_regions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    default_terrain_types TEXT,  -- JSON array
    monster_groups TEXT,  -- JSON array
    backdrop_prefix TEXT
);

-- Special hex locations (cities, dungeons)
CREATE TABLE IF NOT EXISTS hex_special_locations (
    id TEXT PRIMARY KEY,
    q INTEGER NOT NULL,
    r INTEGER NOT NULL,
    location_type TEXT NOT NULL,  -- 'city' or 'dungeon'
    name TEXT NOT NULL,
    region_id TEXT,
    monster_groups TEXT,  -- JSON override
    encounter_types TEXT,  -- JSON array
    backdrop_image TEXT,
    is_visible BOOLEAN DEFAULT 1,
    FOREIGN KEY (region_id) REFERENCES hex_regions(id),
    UNIQUE(q, r)
);

-- Event modifier definitions
CREATE TABLE IF NOT EXISTS hex_events (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    monster_override_chance REAL,  -- 0.0-1.0
    monster_groups TEXT,  -- JSON array
    backdrop_modifier TEXT,
    terrain_effect TEXT,  -- JSON
    duration_type TEXT  -- 'permanent', 'quest', 'timed'
);

-- Active event instances on hexes
CREATE TABLE IF NOT EXISTS hex_active_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    q INTEGER NOT NULL,
    r INTEGER NOT NULL,
    event_id TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (event_id) REFERENCES hex_events(id),
    UNIQUE(q, r, event_id)
);

-- Hex grid mapping to regions
CREATE TABLE IF NOT EXISTS hex_grid (
    q INTEGER NOT NULL,
    r INTEGER NOT NULL,
    region_id TEXT NOT NULL,
    base_terrain TEXT,
    discovered BOOLEAN DEFAULT 0,
    FOREIGN KEY (region_id) REFERENCES hex_regions(id),
    PRIMARY KEY (q, r)
);

-- Seed 4 regional zones
INSERT OR IGNORE INTO hex_regions (id, name, description, default_terrain_types, monster_groups, backdrop_prefix) VALUES
('countryside', 'Countryside', 'Temperate lands, farms, forests, typical Faerûn terrain', 
 '["plains", "forest", "hills"]', 
 '["beast", "humanoid", "fey", "undead"]', 
 'countryside'),
 
('icewind', 'Icewind Dale', 'Frozen tundra, harsh arctic wasteland',
 '["desert", "mountain"]',  -- Using desert for tundra, mountain for peaks
 '["beast", "giant", "elemental", "aberration"]',
 'icewind'),
 
('moonshae', 'Moonshae Isles', 'Celtic-inspired islands, mystical forests',
 '["forest", "hills"]',
 '["fey", "beast", "humanoid", "undead"]',
 'moonshae'),
 
('calimshan', 'Calimshan', 'Desert empire, Arabian Nights aesthetic',
 '["desert", "hills"]',
 '["elemental", "monstrosity", "humanoid", "undead"]',
 'calimshan');

-- Seed event definitions
INSERT OR IGNORE INTO hex_events (id, name, description, monster_override_chance, monster_groups, backdrop_modifier, terrain_effect, duration_type) VALUES
('undead_infestation', 'Undead Infestation', 'Necromantic curse raises the dead', 0.75,
 '["undead"]', 'fog_gray', '{"move_cost_modifier": 1.2}', 'quest'),
 
('demonic_portal', 'Demonic Portal', 'Portal to the Abyss spews demons', 0.9,
 '["fiend"]', 'red_sky', '{"hazards": ["fire", "necrotic"]}', 'quest'),
 
('marauders', 'Marauders', 'Organized raiders terrorize the region', 0.8,
 '["humanoid"]', 'smoke', '{"move_cost_modifier": 1.15}', 'quest'),
 
('legendary_creature', 'Legendary Creature', 'Ancient beast claims territory', 0.5,
 '["dragon", "monstrosity"]', 'lair_effect', '{"lair_actions": true}', 'quest');

-- Seed initial special locations (major cities)
INSERT OR IGNORE INTO hex_special_locations (id, q, r, location_type, name, region_id, monster_groups, encounter_types, backdrop_image, is_visible) VALUES
('waterdeep', 15, 25, 'city', 'Waterdeep', 'countryside', '[]', '["urban", "intrigue"]', 'waterdeep.jpg', 1),
('baldurs_gate', 12, 30, 'city', "Baldur's Gate", 'countryside', '[]', '["urban", "intrigue"]', 'baldurs_gate.jpg', 1),
('neverwinter', 18, 20, 'city', 'Neverwinter', 'countryside', '[]', '["urban", "intrigue"]', 'neverwinter.jpg', 1),
('luskan', 20, 15, 'city', 'Luskan', 'icewind', '["humanoid"]', '["urban", "criminal"]', 'luskan.jpg', 1);
