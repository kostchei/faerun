"""
Database initialization script for Faerun hex region system.
Run this to set up the database with the region tables and seed data.
"""

import sqlite3
import os

def init_database(db_path: str = "faerun_hexes.db"):
    """Initialize the database with region system tables"""
    
    # Read the migration SQL
    migration_path = os.path.join(os.path.dirname(__file__), "migrations", "001_create_hex_regions.sql")
    
    with open(migration_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Connect and execute
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute SQL (split by semicolons for multiple statements)
    for statement in sql.split(';'):
        if statement.strip():
            cursor.execute(statement)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized at {db_path}")
    print("✅ Created tables: hex_regions, hex_special_locations, hex_events, hex_active_events, hex_grid")
    print("✅ Seeded 4 regions: Countryside, Icewind, Moonshae, Calimshan")
    print("✅ Seeded 4 event types")
    print("✅ Seeded 4 cities: Waterdeep, Baldur's Gate, Neverwinter, Luskan")

if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else "faerun_hexes.db"
    init_database(db_path)
