#!/usr/bin/env python3
"""
Generate Manic Miners script triggers for portal tiles (slimy slug holes, tile ID 12)
Parses the tiles{} section from a .dat file and creates drive triggers for each portal location.
"""

import pandas as pd
import re
import sys

def extract_tiles_section(dat_file_path):
    """Extract the tiles{} section from a .dat file"""
    with open(dat_file_path, 'r') as f:
        content = f.read()
    
    # Find tiles section using regex
    tiles_match = re.search(r'tiles\{(.*?)\}', content, re.DOTALL)
    if not tiles_match:
        raise ValueError("Could not find tiles{} section in file")
    
    tiles_content = tiles_match.group(1).strip()
    return tiles_content

def parse_tiles_to_dataframe(tiles_content):
    """Parse tiles content into a pandas DataFrame"""
    # Split by lines and clean up
    lines = [line.strip() for line in tiles_content.split('\n') if line.strip()]
    
    # Each line is comma-separated tile IDs
    tile_data = []
    for row_idx, line in enumerate(lines):
        # Remove trailing comma if present
        line = line.rstrip(',')
        # Split by comma and convert to integers
        row_tiles = [int(tile.strip()) for tile in line.split(',')]
        tile_data.append(row_tiles)
    
    # Create DataFrame
    df = pd.DataFrame(tile_data)
    return df

def find_portal_locations(df, portal_tile_id=12):
    """Find all locations where tile ID equals portal_tile_id (default 12 for slimy slug holes)"""
    portal_locations = []
    
    # Use pandas to find all locations where value equals portal_tile_id
    portal_coords = df.stack().reset_index()
    portal_coords.columns = ['row', 'col', 'tile_id']
    portals = portal_coords[portal_coords['tile_id'] == portal_tile_id]
    
    return portals[['row', 'col']].values.tolist()

def generate_drive_triggers(portal_locations, event_name="vehicleEnteredPortal", cooldown=5.0):
    """Generate block system entries for all portal locations"""
    triggers = []
    
    block_id = 1
    wires = []
    
    for row, col in portal_locations:
        # Generate EventCallEvent block
        event_block_id = block_id
        triggers.append(f"{event_block_id}/EventCallEvent:{row},{col},{cooldown},{event_name}")
        block_id += 1
        
        # Generate TriggerEnter block  
        trigger_block_id = block_id
        triggers.append(f"{trigger_block_id}/TriggerEnter:{row},{col},{cooldown},_,false,true")
        block_id += 1
        
        # Generate wire connecting trigger to event
        wires.append(f"{trigger_block_id}-{event_block_id}")
        
    
    # Add wires section
    if wires:
        triggers.extend(wires)
    
    return "\n".join(triggers)

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_portal_triggers.py <dat_file_path>")
        sys.exit(1)
    
    dat_file_path = sys.argv[1]
    
    try:
        print(f"Parsing {dat_file_path}...")
        
        # Extract and parse tiles
        tiles_content = extract_tiles_section(dat_file_path)
        df = parse_tiles_to_dataframe(tiles_content)
        
        print(f"Map dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
        
        # Find portal locations
        portal_locations = find_portal_locations(df, portal_tile_id=12)
        
        print(f"Found {len(portal_locations)} portal locations:")
        for row, col in portal_locations:
            print(f"  - Row {row}, Col {col}")
        
        if not portal_locations:
            print("No portal tiles (ID 12) found in the map.")
            return
        
        # Generate triggers
        triggers_code = generate_drive_triggers(portal_locations)
        
        # Write to output file
        output_file = dat_file_path.replace('.dat', '_portal_triggers.mms')
        with open(output_file, 'w') as f:
            f.write(triggers_code)
        
        print(f"\nGenerated triggers written to: {output_file}")
        print("\nSample output:")
        print("-" * 50)
        print(triggers_code[:500] + "..." if len(triggers_code) > 500 else triggers_code)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()