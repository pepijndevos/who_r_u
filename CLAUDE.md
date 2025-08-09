# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of Manic Miners level files and comprehensive scripting documentation. Manic Miners is a game where players control miners to explore underground caverns, and this repository contains custom level files (.dat format) with an extremely sophisticated scripting system that can implement complex game mechanics, environmental events, and even complete puzzle games within levels.

## File Structure

- **Level files** (*.dat): ASCII text files with CRLF line endings containing level data, scripting, and map configuration
- **docs/**: Complete documentation for Manic Miners scripting system
  - **_pages/**: Individual documentation pages for all scripting concepts (40+ files)
  - **_media/**: Screenshots and images for documentation
  - **README.md**: Main scripting documentation entry point
- **inspiration/**: Example levels and campaigns demonstrating advanced scripting techniques

## DAT File Format - Complete Section Specification

DAT files use a structured text format with sections enclosed in curly braces. **Order matters** for some sections.

### Required Sections (in typical order):
1. `comments{}` - Developer comments and metadata
2. `info{}` - Basic level configuration
3. `tiles{}` - Tile layout as comma-separated values (tile IDs)
4. `height{}` - Height map data (elevation for each tile)
5. `resources{}` - Crystal, ore, and stud placement (crystals:/ore:/studs: subsections)
6. `objectives{}` - Win conditions and requirements
7. `buildings{}` - Building placement and properties
8. `landslidefrequency{}` - Landslide configuration parameters
9. `lavaspread{}` - Lava spread behavior settings
10. `miners{}` - Starting miner placement and properties
11. `briefing{}` - Mission briefing text (displayed at level start)
12. `briefingsuccess{}` - Success message text
13. `briefingfailure{}` - Failure message text
14. `vehicles{}` - Vehicle placement and properties
15. `creatures{}` - Creature placement and spawn points
16. `blocks{}` - Visual block system data (used with scripting)
17. `script{}` - **The scripting code section**

### Key Info Section Parameters:
- `biome:rock|lava|ice` - Environmental theme
- `rowcount:N` / `colcount:N` - Map dimensions (critical for coordinate system)
- `oxygen:initial/max` - Air system configuration
- `levelname:Name` / `creator:Name` - Metadata
- `opencaves:row,col/row,col/...` - Initially visible areas
- `erosionscale:factor` - Lava erosion speed multiplier

## Recommended Workflow for Scripting Tasks

### Before Writing Any Script Code:
1. **Verify map dimensions** from `info{}` section (rowcount/colcount)
2. **Read existing tile layout** from `tiles{}` section to understand coordinate system
3. **Check resource placement** from `resources{}` section 
4. **Identify object references** from `miners{}/buildings{}/vehicles{}` sections

### When Writing Scripts:
1. **Start with variable declarations** at top level (no semicolons)
2. **Write event chains** before triggers that reference them
3. **Use Level Editor Script Interface** to verify coordinates under mouse cursor
4. **Test frequently** - scripts are interpreted at runtime, no compilation needed

### Critical Validation Steps:
1. **Coordinate bounds checking**: Ensure row < rowcount and col < colcount
2. **Syntax verification**: Triggers have NO semicolons, events in chains DO have semicolons
3. **Object reference validation**: Confirm miners/buildings exist at specified coordinates/IDs
4. **Accessibility verification**: Ensure players can reach scripted locations

### Debugging When Scripts Fail:
1. **Check Level Editor → Script Interface → Show Logs** for error messages
2. **Verify semicolon rules**: Most common failure is semicolons on triggers
3. **Confirm square brackets**: All trigger events must be in `[event]` format
4. **Test coordinate validity**: Use exact row/col from tiles grid, not file line numbers

## Scripting System - Deep Technical Reference

### Quick Syntax Reference (For Fast Lookup)
```mms
# TRIGGERS (NO semicolons, square brackets around events)
if(condition)[event]                    # Single-fire trigger  
when(condition)[event]                  # Repeating trigger
if(condition)((check))[trueevent][falseevent]  # Conditional trigger

# EVENT CHAINS (semicolons required, blank line ends chain)
myChain::;
event1;
event2;
((condition))event3;

# VARIABLE DECLARATIONS (at top level, NO semicolons)
int myVar=5
string myMsg="Hello"
miner myMiner=0

# COMMON EVENTS (inside event chains only)
msg:"Text";                            # Display message
place:row,col,tileID;                  # Place tile
win:"Victory!";                        # End level successfully
```

### Critical Syntax Rules (Most Important)
1. **NO SPACES** at line beginnings, endings, or in middle of lines (except in strings)
2. **NO SPACES** after semicolons (most common error causing script failures)
3. All events in event chains **MUST** end with semicolon `;`
4. Triggers do **NOT** end with semicolons
5. Coordinates always in **row,col** order (Y,X format, not X,Y)
6. Blank lines end event chains (comments do not count as blank lines)
7. `#` character **always** starts a comment regardless of position

### Variable Types and Declarations
```mms
# Object References
arrow MyArrow=red                    # UI highlighting (colors: black,blue,darkgreen,green,red,yellow,white)
building MyHQ=3,4                   # Reference to existing building at row 3, col 4
creature MyMonster=2                # Reference to existing creature ID 2
miner Charlie=3                     # Reference to existing miner ID 3  
vehicle BigBoye=2                   # Reference to existing vehicle ID 2
timer MyTimer=1.0,2.0,5.0,eventchain # Delay,min,max,event chain to call

# Data Types
bool HasFinished=true               # Boolean values
int MyInteger=5                     # Integer numbers (cannot initialize negative values directly)
float MyFloat=2.6                   # Floating-point numbers
string MyMsg="Hello World"          # Text strings (spaces allowed inside quotes)
intarray MyArray                    # Integer arrays (auto-growing, 0-based indexing)
```

### Trigger Format and Types
```mms
# Single-fire triggers (remove after first activation)
if(TRIGGER)((CONDITION))[TRUE_EVENT][FALSE_EVENT]

# Repeating triggers (fire every time condition is met)  
when(TRIGGER)((CONDITION))[TRUE_EVENT][FALSE_EVENT]

# Examples:
if(time:60.0)[win:"Victory!"]                        # Win after 60 seconds
when(drill:5,10)[msg:"Wall destroyed!"]              # Message when wall drilled
when(walk:12,15,charlie)((charlie.health<50))[heal:charlie,25] # Heal when injured Charlie walks on tile
```

### Available Classes and Methods

#### Building Class (docs/_pages/ClassesBuildings.md)
- **Trigger Properties**: `built`, `click`, `dead`, `hurt`, `levelup`, `new`, `poweroff`, `poweron`
- **Read Properties**: `col`, `health/hp`, `ispowered/power/powered`, `level`, `row`, `tile/tileid`, `X/Y/Z`
- **Collections**: `BuildingCanteen_C`, `BuildingDocks_C`, `BuildingElectricFence_C`, etc. (13 building types)

#### Creature Class (docs/_pages/ClassesCreatures.md)  
- **Trigger Properties**: `dead`, `new`, `wake`
- **Read Properties**: `col`, `eaten`, `health/hp`, `id`, `row`, `tile/tileid`, `X/Y/Z`
- **Collections**: `CreatureBat_C`, `CreatureRockMonster_C`, `CreatureIceMonster_C`, etc. (6 creature types)

#### Miner Class (docs/_pages/ClassesMiners.md)
- **Trigger Properties**: `dead`, `new`, `click`, `hurt`, `levelup`  
- **Read Properties**: `col`, `health/hp/stamina`, `level`, `row`, `tile/tileid`, `X/Y/Z`
- **Special Collection**: `miner` (trigger-only collection for all miners)

#### Vehicle Class (docs/_pages/ClassesVehicles.md)
- **Trigger Properties**: `click`, `dead`, `driven`, `hurt`, `new`, `upgrade`
- **Read Properties**: `col`, `driver/driverid`, `health/hp`, `id`, `row`, `tile/tileid`, `X/Y/Z`
- **Collections**: `VehicleCargoCarrier_C`, `VehicleChromeCrusher_C`, etc. (12 vehicle types)

#### Arrow Class (docs/_pages/ClassesArrow.md)
- **Events**: `hidearrow:ARROW`, `highlight:ROW,COL,ARROW`, `highlightarrow:ROW,COL,ARROW`, `showarrow:ROW,COL,ARROW`

#### Timer Class (docs/_pages/ClassesTimer.md)
- **Events**: `starttimer:name`, `stoptimer:name`
- **Declaration**: `timer MyTimer=DELAY,MIN,MAX,EVENTCHAIN`

### Core Events Reference (docs/_pages/Events.md)

#### Tile and Map Modification
- `place:ROW,COL,TILEID` - Place any tile (see docs/_pages/DATTileReference.md for tile IDs)
- `drill:ROW,COL` - Drill/collapse tile

#### Object Spawning and Management  
- `emerge:ROW,COL,DIRECTION,COLLECTION,DISTANCE` - Spawn creature from wall
- `flee:OBJECT,ROW,COL` - Make creature flee to location
- `kill:VARIABLE` - Kill/teleport object
- `heal:OBJECT,AMOUNT` - Heal object

#### Game Control
- `win:MsgStr` / `lose:MsgStr` - End level with message
- `msg:MsgStr` / `qmsg:MsgStr` - Display message (qmsg requires acknowledgment)
- `pan:ROW,COL` - Pan camera to location
- `pause` / `unpause/resume` - Game flow control
- `shake:VALUE` - Camera shake effect
- `sound:MySoundName` - Play .ogg sound file

#### Resource and Object Control
- `drain:NUM` - Drain crystals from player
- `enable:COLLECTION` / `disable:COLLECTION` - Enable/disable object types
- `save*` events - Save last created object to variable

#### Math Operations
- `+`, `+=`, `-`, `-=`, `*`, `*=`, `//`, `/=` - Arithmetic operations

#### Spawning Control (docs/_pages/Events.md)
- `addrandomspawn:COLLECTION,MINTIME,MAXTIME` - Configure random creature spawning
- `startrandomspawn:Collection` / `stoprandomspawn:Collection` - Control random spawning
- `spawncap:Collection,MIN,MAX` / `spawnwave:Collection,MIN,MAX` - Control spawn limits

#### Timing Events
- `wait:GAME_SECONDS` - Wait (affected by game speed)
- `truewait:REAL_SECONDS` - Wait (real time, not affected by game speed)

### Advanced Event Chain Patterns

#### Special Event Chains
- `init::` - Called once at level start (before any triggers)
- `tick::` - Called every frame (avoid using - performance impact)

#### Event Chain Syntax
```mms
myEventChain::;                     # Event chain declaration
event1;                            # First event  
event2;                            # Second event
((condition))event3;               # Conditional event
((condition))[trueevent][falseevent]; # Conditional with both branches

                                   # Blank line ends event chain
```

#### Special Event Modifiers  
- `?` - Random event selection within event chains
- `~` - Failed emerge event handling

### Trigger Types and Patterns (docs/_pages/Triggers.md)

#### Tile-based Triggers
- `built:(ROW,COL)` - Building construction
- `change:(ROW,COL[,TILEID])` - Tile change detection  
- `click:(ROW,COL)` - Player click on tile
- `drill:(ROW,COL)` - Wall drilling/collapse
- `drive:(ROW,COL[,NAME])` - Vehicle movement
- `enter:(ROW,COL[,NAME])` - Object entry detection
- `hover:(ROW,COL)` - Mouse hover
- `laser:(ROW,COL)` / `laserhit:(ROW,COL)` - Laser events
- `reinforce:(ROW,COL)` - Wall reinforcement
- `walk:(ROW,COL[,NAME])` - Miner movement

#### Time-based Triggers
- `time:(SECONDS)` - Elapsed time trigger

### Conditions and Logic (docs/_pages/Conditions.md)
```mms
# Comparison operators
>  >=  <  <=  ==  !=

# Usage patterns - these are CONDITIONS in event chains, not standalone triggers
((variable>5))event;                # Simple condition in event chain
((miner.health<=25))heal:miner,50;  # Object property condition in event chain
((crystals>=100))win:"Collected enough crystals!"; # Macro condition in event chain
```

### Reserved Words and Macros (docs/_pages/ReservedWords.md)

#### Core Keywords
- `if`, `when`, `init`, `tick`, `true`, `false`, `return`
- Data types: `bool`, `int`, `float`, `string`, `intarray`, `arrow`, `building`, `creature`, `miner`, `timer`, `vehicle`
- Directions: `A` (auto), `N`, `S`, `E`, `W`
- Colors: `black`, `blue`, `darkgreen`, `green`, `red`, `yellow`, `white`

#### Important Macros (200+ available)
- `air`, `crystals`, `ore`, `studs`, `time`, `clock` - Game state values
- `miners`, `vehicles`, `buildings`, `creatures`, `hostiles`, `monsters` - Object counts
- `random(min)(max)` - Random number generation

### Complex Scripting Patterns from Examples

#### State Management (lights_out.dat pattern)
```mms
bool state11=false
bool state12=false  
bool setupdone=false

init::;
((random(0)(1)==0))togglechain11all;  # Random initialization
setupdone=true;
```

#### Progressive Tutorial System (inspiration/Quadrant_85_v108 examples)
```mms
int hintstage=0
# This is showing a PATTERN, not correct syntax - needs event chain:
when(click:10,15)((hintstage==0))[hintEvent1]
when(click:10,15)((hintstage==1))[hintEvent2]

hintEvent1::;
hintstage+=1;
msg:"First hint";

hintEvent2::;
hintstage+=1;
msg:"Second hint";
```

#### Multi-trigger Safety System (inspiration/Seams of Knowledge examples)  
```mms
if(enter:67,13)[safetyTrigger]
if(enter:67,12)[safetyTrigger]  
if(enter:67,11)[safetyTrigger]
safetyTrigger::;
((safetyReached==false))safety;
```

#### Complex Mathematical Operations (A_Crazy_Maze.dat)
```mms
# Custom division algorithm (division not directly supported)
calcPos::;
placeX=23;
placeY=23;
tempY=buildCounter;
divCounter=0;
((tempY>=7))divCounter+=1;
((tempY>=7))tempY-=7;
((tempY>=7))divCounter+=1;
((tempY>=7))tempY-=7;
# Repeated to implement division by 7
```

#### Dynamic Array Management and Tile Rotation
```mms
intarray CardArrayToPlace
intarray rotBuffer

rotateCard::;
rotBuffer[0]=CardArrayToPlace[2];
CardArrayToPlace[2]=CardArrayToPlace[17];  
CardArrayToPlace[17]=CardArrayToPlace[33];
# Complex pattern for 90-degree tile rotation
```

## Critical Language Limitations (NON-STANDARD! DO NOT ASSUME TYPICAL PROGRAMMING PATTERNS!)

**⚠️ WARNING: This scripting language violates most standard programming conventions. DO NOT assume familiar patterns will work!**

### Semicolon Rules (COMPLETELY OPPOSITE to Most Programming Languages)
- **Events in event chains MUST end with semicolon** - This is opposite to most languages where semicolons separate statements
- **Triggers NEVER have semicolons** - Even though they look like statements  
- **NO SPACES after semicolons** - Will cause script compilation failure
- **Blank lines end event chains** - Not semicolons like in typical languages

**CRITICAL ERROR PATTERN**: Adding semicolons to triggers breaks ALL script functionality!

```mms
# WRONG - This breaks everything:
when(rock.click)[msg:"Hello"];     # ❌ Semicolon kills trigger completely

# CORRECT:
myChain::;
event1;        # ✅ Semicolon required in event chains
event2;        # ✅ Semicolon required in event chains  
               # Blank line ends chain

if(time:60)[win:"Victory!"]        # ✅ NO semicolon on triggers ever!
```

**DO NOT TRUST YOUR PROGRAMMING INSTINCTS - This language is intentionally non-standard!**

### Expression and Parameter Limitations (STRICT - NO ASSUMPTIONS!)
- **No complex expressions** - Cannot use `((health + stamina) > 100)` - must split into separate operations
- **No nested macros** - Cannot use `random(0)(miners)` if `miners` is a macro
- **No variables in trigger parameters** - Cannot use `if(time:myTimeVar)` - must use literal values
- **No arithmetic in parameters** - Cannot use `place:row+1,col,5` - must calculate separately

**OBSERVED FAILURE PATTERNS:**
- Assuming familiar trigger syntax would work (e.g., `when(change:crystals)` - doesn't exist!)
- Using standard programming conditions without checking documentation first
- Trying complex expressions that look like they should work but don't

```mms
# WRONG - These will NOT work (REAL FAILURES FROM TESTING):
when(change:crystals)[event]               # ❌ change: is for tiles, not resources!  
if(time:myDelayVar)[win];                    # ❌ Variables not allowed in trigger params
when(walk:playerRow,playerCol)[msg];         # ❌ Variables not allowed in coordinates  
((health+stamina>100))event;               # ❌ Complex expressions not supported
emerge:5,6,N,random(0)(2),1                # ❌ Nested macros not allowed

# CORRECT - Use only documented patterns:
when(crystals>=8)[event]                   # ✅ Resource macro with literal comparison

# Event chain for coordinate calculation:
calculateCoords::;
myRow=5;
myCol=6;                          # ✅ Calculate coordinates separately (no spaces after semicolon)
totalHealth=health;
totalHealth+=stamina;  # ✅ Split complex operations (no spaces after semicolon)
((totalHealth>100))event;                # ✅ Simple variable comparison
if(time:30.0)[win:"Victory!"]              # ✅ Literal values only in triggers
```

**GOLDEN RULE: If a pattern isn't explicitly documented with examples, assume it doesn't work!**

### Variable and Object Limitations
- **No variable scope** - All variables are global
- **No local variables** - Cannot declare variables inside event chains
- **One variable per object** - Cannot have `miner bob=1; miner alice=1;` (both pointing to same miner)
- **No object creation via script** - Can only reference existing objects placed in DAT sections

## Complete Error Reference and Performance Guide

### The 10 Most Common Script Failures (In Order of Frequency)
1. **Semicolons on triggers** - `if(condition)[event];` breaks ALL script functionality
2. **Missing square brackets** - `when(click)msg` should be `when(click)[msg]`
3. **Spaces after semicolons** - `event1; event2;` should be `event1;event2;`
4. **Wrong coordinates** - Using file line numbers instead of tiles grid positions  
5. **Variables in trigger parameters** - `if(time:myVar)` not supported, use literals only
6. **Complex expressions** - `((health+stamina>100))` not supported, split into separate operations
7. **Row,col vs col,row confusion** - Always use row,col (Y,X) format
8. **Events at top level** - Variable assignments must be inside event chains
9. **Object reference errors** - Referencing miners/buildings that don't exist
10. **Coordinate bounds violations** - Using row/col values >= rowcount/colcount

### Syntax Error Patterns (REAL FAILURES FROM TESTING)
```mms
# WRONG - These patterns ALL break scripts:
when(rock.click)msg:"Hello";              # ❌ Semicolon + missing brackets
when(change:crystals)[event]              # ❌ change: doesn't exist for resources  
if(time:myDelayVar)[win];                 # ❌ Variables not allowed in trigger params
place:28,col,tile;                        # ❌ Row 28 in 22-row map = impossible
myVar=5;                                  # ❌ Variable assignment at top level

# CORRECT - Use these patterns:
when(rock.click)[msg:"Hello"]             # ✅ No semicolon, square brackets
when(crystals>=8)[event]                  # ✅ Resource macro with literal comparison  
if(time:30.0)[win:"Victory!"]             # ✅ Literal values in trigger parameters
place:12,col,tile;                        # ✅ Verified coordinate within map bounds

# Variable assignment in event chain:
init::;
myVar=5;                                  # ✅ Assignment inside event chain
```

### Performance and Technical Limitations
- **Minimize macro usage** in trigger conditions (evaluated every tick)
- **Use `if` instead of `when`** when single execution is sufficient
- **Avoid `tick::` event chain** - causes severe performance impact
- **Limit tile modifications** - ~630 tiles per trigger context maximum
- **Reentrancy**: `when` triggers and timers can interrupt themselves (~890 call limit)
- **Water/lava restrictions**: Cannot mix with other tile modifications in same trigger
- **Unit creation**: Only player can create miners/buildings/vehicles

## Development Workflow

### File Handling
- DAT files are plain text with Windows CRLF line endings
- Use any text editor, but preserve CRLF format
- Supported encodings: ANSI 8-bit, UTF8 BOM, UTF16LE BOM, UTF16BE BOM

### Debugging  
- Level Editor provides Script Interface button for row/col/tile ID display
- Game logs show script execution and errors (limited buffer size)
- Located at: Level Editor → Script Interface → Show Logs

### Testing
- No build/test commands needed - scripts are interpreted at runtime
- Test in-game using Level Editor
- Reference examples in ManicMiners\Levels\DEMO\Scripts installation folder

## Documentation Cross-References

### Essential Documentation Files
- **docs/_pages/ScriptingStructure.md**: Overall script organization
- **docs/_pages/Events.md**: Complete event reference with examples
- **docs/_pages/Triggers.md**: All trigger types and patterns  
- **docs/_pages/Variables.md**: Variable types and scope rules
- **docs/_pages/Conditions.md**: Logic and comparison operations
- **docs/_pages/Classes*.md**: Object-oriented programming reference
- **docs/_pages/DATFileFormat.md**: Complete file format specification
- **docs/_pages/ReservedWords.md**: All 200+ reserved words and macros
- **docs/_pages/DATTileReference.md**: Tile ID reference for `place:` events

### Example Files by Complexity Level
- **Simple**: cabbage.dat, unwilling_worker.dat  
- **Intermediate**: lights_out.dat (state management)
- **Advanced**: inspiration/Quadrant_85_v108/*.dat (environmental events, tutorials)
- **Expert**: inspiration/A_Crazy_Maze.dat (complete puzzle game implementation)

## Tile ID Reference for Refactoring (docs/_pages/DATTileReference.md)

Understanding tile IDs is crucial for refactoring level data and `place:` events in scripts.

### Floor Tiles (Allow Movement)
```
0   - Invalid texture (DO NOT USE - causes warnings)
1   - Ground (standard floor)
2-5 - Rubble levels 1-4 (from wall collapses)
6   - Lava (special tile - placement restrictions apply)
7-10- Erosion levels 4-1 (lava erosion stages)
11  - Water (special tile - placement restrictions apply)
12  - Slimy slug hole
13-25 - Power path variants (in progress, building, powered states)
60-63 - Fake rubble 1-4 (decorative, no ore when cleared)
```

### Wall Tiles (Block Movement, 2-tiles thick)
Each wall type has 4 variants (use **regular** for normal placement):

**Dirt (Easiest to drill)**
```
26 - Dirt regular (use this for scripting)
27 - Dirt corner (auto-generated by engine)
28 - Dirt edge (auto-generated by engine)  
29 - Dirt intersect (auto-generated by engine)
```

**Loose Rock (Medium difficulty)**
```
30 - Loose rock regular (use this for scripting)
31-33 - Corner/edge/intersect (auto-generated)
```

**Hard Rock (Hard to drill)**
```
34 - Hard rock regular (use this for scripting)
35-37 - Corner/edge/intersect (auto-generated)
```

**Solid Rock (Indestructible)**
```
38 - Solid rock regular (map borders, unbreakable walls)
39-41 - Corner/edge/intersect (auto-generated)
```

**Resource Seams**
```
42 - Crystal seam regular (contains crystals)
43-45 - Crystal seam corner/edge/intersect
46 - Ore seam regular (contains ore)  
47-49 - Ore seam corner/edge/intersect
50 - Recharge seam regular (restores air)
51-53 - Recharge seam corner/edge/intersect
```

**Special Tiles**
```
54-57, 59 - Biome specific walls (vary by biome:rock/lava/ice)
58 - Roof
64-65 - Cliff types 1-2 (experimental, single-tile thick walls)
```

### Important Tile Modifiers
- **+50**: Reinforced walls (cannot cause landslides, monsters can't emerge)
- **+100**: Undiscovered cavern (auto-added by editor, removed when discovered)

### Key Rules for Refactoring
1. **Use regular variants** (26,30,34,38,42,46,50) - engine auto-converts to corners/edges
2. **Walls must be 2-tiles thick** or they collapse to rubble  
3. **Water (11) and Lava (6)** have special placement restrictions (see water/lava mixing rules)
4. **Never use Tile 0** - causes engine warnings
5. **Script access**: Tiles 1-175 available via `place:` events
6. **Map borders**: Usually solid rock (38) for containment

### Common Refactoring Patterns
```mms
# These are EVENT examples that go inside event chains:
# Wall creation (use regular variants)
place:row,col,30;        # Loose rock wall
place:row,col,34;        # Hard rock wall  
place:row,col,38;        # Solid rock (unbreakable)

# Floor creation  
place:row,col,1;         # Standard ground
place:row,col,2;         # Rubble level 1

# Resource seams
place:row,col,42;        # Crystal seam
place:row,col,46;        # Ore seam
place:row,col,50;        # Recharge seam (air)

# Special effects (separate triggers for water/lava)
place:row,col,11;        # Water (only water in this trigger)
place:row,col,6;         # Lava (only lava in this trigger)
```

## Spatial Reasoning and Grid Manipulation

Understanding spatial relationships is crucial for effective refactoring of tile placement and coordinate-based scripts.

### Coordinate System (MOST CRITICAL!)
- **Always row,col (Y,X)** - not the typical X,Y convention
- **Row = Y-axis (vertical)**, **Col = X-axis (horizontal)**  
- **Origin (0,0) = top-left corner**
- Coordinates increase: **right** (col+) and **down** (row+)

**⚠️ CRITICAL COORDINATE RULE: NEVER use file line numbers for coordinates!**

**CORRECT**: Count rows in the tiles grid starting from 0:
```
tiles{
38,38,38...    # This is row 0
38,38,38...    # This is row 1  
38,38,38...    # This is row 2
...
38,111,111...  # If this is the 13th data row, this is row 12
}
```

**CRITICAL ERRORS OBSERVED:**
- Used `place:28,col,tile` in a 22-row map (row 28 doesn't exist!)
- Confused file line numbers with actual grid coordinates
- Failed to verify coordinates exist within map bounds (0 to rowcount-1)

**MANDATORY COORDINATE VERIFICATION:**
1. **Always count from tiles{ section start** - Ignore file line numbers completely
2. **Verify bounds**: row must be 0 to (rowcount-1), col must be 0 to (colcount-1)  
3. **Cross-reference with existing tile data** before using coordinates in scripts
4. **Use Level Editor Script Interface** to display row/col under mouse cursor for exact positioning

### Grid Visualization for Pattern Recognition
```
       0   1   2   3   4  (cols)
    0  38  38  38  38  38
    1  38   1   1   1  38  (rows)
    2  38   1  30   1  38  
    3  38   1   1   1  38
    4  38  38  38  38  38
```

### Spatial Variables and Calculations
Variables ARE allowed in place events, but arithmetic expressions are NOT:

```mms
# CORRECT - Variables allowed in events (must be inside event chain)
int targetRow=5
int targetCol=10

placeWall::;
place:targetRow,targetCol,30;        # Works: variables in place events

# CORRECT - Calculate first, then use variables (must be in event chain)
int roomStartRow=5
int roomStartCol=8
int innerRow=0
int innerCol=0

calculateAndPlace::;
innerRow=roomStartRow;
innerRow+=2;   # Calculate offset separately
innerCol=roomStartCol;
innerCol+=3;   # Calculate offset separately  
place:innerRow,innerCol,42;          # Place crystal seam at calculated position

# WRONG - Arithmetic expressions not allowed in event parameters
place:roomStartRow+2,roomStartCol+3,42;  # ERROR: Cannot do arithmetic in parameters
```

### Script Structure Rules (Critical!)
At the **top level** of script section, only these are allowed:
1. **Variable declarations**: `int myVar=5`
2. **Triggers**: `if(condition)[event]` or `when(condition)[event]`  
3. **Event chains**: `myChain::;`

**Variable assignments are EVENTS** and must be inside event chains!

### Directional Movement Patterns
```mms
# Variable declarations at top level
int centerRow=10
int centerCol=15
int northRow=0
int southRow=0
int westCol=0
int eastCol=0

# Calculations and placement inside event chain
init::;
northRow=centerRow;
northRow-=1;        # North: row-1
southRow=centerRow;
southRow+=1;        # South: row+1  
westCol=centerCol;
westCol-=1;          # West: col-1
eastCol=centerCol;
eastCol+=1;          # East: col+1
place:northRow,centerCol,1;             # North tile
place:southRow,centerCol,1;             # South tile
place:centerRow,westCol,1;              # West tile  
place:centerRow,eastCol,1;              # East tile
```

### Common Spatial Patterns for Refactoring

**⚠️ COORDINATE CALCULATION CRITICAL ERRORS LEARNED:**
1. **File line confusion**: Used line 28 for coordinate row 28 in 22-row map - IMPOSSIBLE!
2. **Bounds checking failure**: Never verified coordinates exist within rowcount/colcount limits
3. **Spatial reasoning errors**: Placed objects outside accessible areas, in water, behind undrillable walls

**MANDATORY VERIFICATION PROCESS:**
1. **Count tiles grid rows starting from 0** - ignore all file line numbers
2. **Check map bounds**: Ensure row < rowcount and col < colcount from info section
3. **Verify tile accessibility**: Check surrounding tiles aren't blocking player access
4. **Cross-reference existing data**: Look at current tile/resource layout before modification

#### Rectangular Area Filling (With Proper Verification)
```mms
# Variable declarations at top level - VERIFY BOUNDS FIRST!
# For 22x22 map: rowcount:22 means rows 0-21, colcount:22 means cols 0-21
int minRow=5        # ✅ 5 < 22, valid
int maxRow=8        # ✅ 8 < 22, valid  
int minCol=10       # ✅ 10 < 22, valid
int maxCol=13       # ✅ 13 < 22, valid

# Event chain to fill rectangle - manual coordinate verification
fillRectangle::;
place:5,10,1;
place:5,11,1;
place:5,12,1;
place:5,13,1;     # Row 5, cols 10-13: VERIFIED
place:6,10,1;
place:6,11,1;
place:6,12,1;
place:6,13,1;     # Row 6, cols 10-13: VERIFIED
place:7,10,1;
place:7,11,1;
place:7,12,1;
place:7,13,1;     # Row 7, cols 10-13: VERIFIED  
place:8,10,1;
place:8,11,1;
place:8,12,1;
place:8,13,1;     # Row 8, cols 10-13: VERIFIED

# Trigger to call rectangle filling
if(time:10.0)[fillRectangle]
```

#### Symmetric Pattern Creation
```mms
# Variable declarations at top level
int centerRow=15
int centerCol=20
int offset=3
int topRow=0
int bottomRow=0
int leftCol=0
int rightCol=0

# Event chain to create symmetric cross
createCross::;
topRow=centerRow;
topRow-=offset;
bottomRow=centerRow;
bottomRow+=offset;
leftCol=centerCol;
leftCol-=offset;
rightCol=centerCol;
rightCol+=offset;
place:topRow,centerCol,42;              # Top crystal
place:bottomRow,centerCol,42;           # Bottom crystal (mirror)
place:centerRow,leftCol,42;             # Left crystal  
place:centerRow,rightCol,42;            # Right crystal (mirror)
```

#### Room Template System
```mms
# Variable declarations at top level
int roomRow=10
int roomCol=15
int roomWidth=8
int roomHeight=6
int doorRow=0
int chestRow=0
int chestCol=0

# Event chain to setup room
setupRoom::;
doorRow=roomRow;
doorRow+=3;            # Door at middle of left wall
chestRow=roomRow;
chestRow+=1;          # Chest near top-right
chestCol=roomCol;
chestCol+=6;
place:doorRow,roomCol,1;                # Door opening
place:chestRow,chestCol,42;             # Crystal chest location
```

### Spatial Debugging Best Practices (LEARNED FROM FAILURES)

**CRITICAL PRE-FLIGHT CHECKLIST:**
1. **Verify map dimensions** from info{} section first
2. **Count tiles{} grid rows manually** starting from 0
3. **Cross-reference coordinates** with existing tile/resource data
4. **Check accessibility**: Ensure path exists from start to target location

**DESCRIPTIVE VARIABLE NAMING WITH VERIFICATION:**
```mms
# For 22x22 map - ALWAYS COMMENT BOUNDS CHECK!
int bridgeStartRow=5     # ✅ 5 < 22, valid row
int bridgeEndRow=15      # ✅ 15 < 22, valid row  
int caveEntranceCol=20   # ✅ 20 < 22, valid col
int treasureRoomCol=18   # ✅ 18 < 22, valid col (NOT 35 in small map!)
```

**GROUP COORDINATES WITH BOUNDS VERIFICATION:**
```mms
# Treasure cave bounds - VERIFIED AGAINST 22x22 MAP
int caveMinRow=14        # ✅ 14 < 22, valid
int caveMaxRow=16        # ✅ 16 < 22, valid
int caveMinCol=17        # ✅ 17 < 22, valid  
int caveMaxCol=19        # ✅ 19 < 22, valid
```

**COMMENT WITH ACTUAL COORDINATE VALUES:**
```mms
place:12,17,1;                        # Bridge tile at row 12, col 17 (VERIFIED)
place:15,18,42;                       # Crystal in treasure cave at row 15, col 18 (VERIFIED)
```

### Map Boundary Considerations
Always verify coordinates are within map bounds:
- Maximum row: `rowcount-1` (from info section)
- Maximum col: `colcount-1` (from info section)  
- Map borders typically use solid rock (38) for containment


## Critical Level Design Lessons Learned

### Miners Section Format (IMPORTANT!)
**WRONG - Text-based format doesn't work properly:**
```
miners{
levels:1,1
names:Rock,Crystal  
emergepoints:11,11/11,12
beamuppoints:
}
```

**CORRECT - Editor generates world coordinates:**
```
miners{
ID=0,Translation: X=3590.573 Y=3314.831 Z=52.150 Rotation: P=0.000000 Y=37.239300 R=0.000000 Scale X=1.000 Y=1.000 Z=1.000,Drill/
ID=1,Translation: X=3682.902 Y=3302.410 Z=52.150 Rotation: P=0.000000 Y=-5.586735 R=0.000000 Scale X=1.000 Y=1.000 Z=1.000,Drill/
}
```

**Key Points:**
- Use the Level Editor to place miners, don't try to write coordinates manually
- Editor automatically assigns proper world coordinates (X,Y,Z in world units, not tiles)
- Miners get `Drill/` equipment by default when placed in editor
- `emergepoints` format may not work as expected - use editor placement instead

### Essential Gameplay Requirements

#### Tool Store Requirement
- **MUST have a Tool Store building** for miners to drop off resources
- Without Tool Store: Miners need shovels to dig ore → build teleport pad → then build Tool Store
- Tool Stores must be adjacent to power paths for functionality
- Resources are typically placed in walls (ore seams, crystal seams) not loose on ground

#### Resource Placement Patterns
- **Primary**: Place resources in walls using seam tiles (42=crystals, 46=ore, 50=recharge)
- **Secondary**: Crystals can be placed in undiscovered caves for exploration rewards
- **Avoid**: Placing resources freely on ground tiles (not typical gameplay)

#### Power System
- Buildings require power paths to function
- Power paths connect buildings to Power Station
- Without proper power infrastructure, buildings won't work

### Level Editor vs Manual Creation
**Recommendation**: Use Level Editor for placing:
- Miners (complex world coordinates)
- Buildings (placement validation and power requirements)
- Vehicles (similar coordinate complexity)

**Safe for manual editing**:
- Tile layout (tiles section)
- Resources (crystals/ore/studs sections)
- Scripting (script section)
- Basic info parameters

### Script Variable References
When referencing objects placed by editor:
```mms
# Miners use ID numbers from editor
miner rock=0        # References ID=0 from miners section
miner crystal=1     # References ID=1 from miners section

# Buildings use row,col coordinates
building toolStore=10,15    # Building at that tile position
```


### Level Design Best Practices
- **Use Level Editor for complex placement** (miners, buildings, vehicles)
- **Ensure Tool Store exists** - Required for resource collection workflow
- **Plan power infrastructure** - Buildings need power paths to function
- **Place resources in walls** using seam tiles (42=crystals, 46=ore, 50=recharge)
- **Verify accessibility** - Players must be able to reach all scripted locations

### Community Resources
- **Online Documentation**: https://manicminers.github.io/docs/#/README
- **Discord Support**: Manic Miners Discord #Scripting channel
- **Game Website**: https://manicminers.baraklava.com/
- **Wiki**: https://manicminers.fandom.com/

---

## Summary: The Five Most Critical Rules for Success

1. **TRIGGERS NEVER HAVE SEMICOLONS**: `if(condition)[event]` not `if(condition)[event];`
2. **COORDINATES ARE ROW,COL (Y,X)**: Count from tiles{} grid start, ignore file line numbers
3. **EVENTS NEED SEMICOLONS IN CHAINS**: `msg:"Hello";` inside event chains, never at top level
4. **VARIABLES AT TOP, ASSIGNMENTS IN CHAINS**: Declare variables at top level, assign in event chains
5. **SQUARE BRACKETS AROUND ALL TRIGGER EVENTS**: `when(click)[msg:"Hello"]` not `when(click)msg:"Hello"`

**GOLDEN RULES**: 
- If it's not explicitly documented, assume it doesn't work
- When in doubt, check the Level Editor Script Interface for coordinates
- Test early and often - the language is unforgiving of syntax errors