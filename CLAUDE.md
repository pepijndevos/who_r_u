# CLAUDE.md - Manic Miners Scripting Syntax Guide

This repository contains Manic Miners level files (.dat format) with scripting system.

## DAT File Structure

DAT files have sections in curly braces. Key sections:
- `info{}` - Map dimensions (rowcount/colcount), biome, level name
- `tiles{}` - Tile layout as comma-separated IDs
- `resources{}` - Crystal/ore placement
- `miners{}/buildings{}/vehicles{}` - Object placement
- `script{}` - **Scripting code**

## Workflow
1. **Check map dimensions** from `info{}` (rowcount/colcount)
2. **Read tile layout** from `tiles{}` for coordinates
3. **Verify object placement** before referencing in scripts
4. **Test coordinates** within bounds (0 to rowcount-1, 0 to colcount-1)

## Reading DAT Files
**IMPORTANT**: Use `sed -n '/^script{/,/^}/p' filename.dat` to extract script sections, or `cat filename.dat` for full file. The Read tool has issues with .dat files.

## Core Syntax Rules

**1. TRIGGERS = NO SEMICOLONS + SQUARE BRACKETS**
**2. EVENTS = SEMICOLONS + NO SPACES AFTER** 
**3. CONDITIONS = SINGLE ONLY, DOUBLE PARENTHESES (())**
**4. VARIABLES = TOP LEVEL DECLARATIONS ONLY**

### Trigger Syntax (6 Official Forms Only)
```mms
if(TRIGGER)[EVENT]                              # Fire once
when(TRIGGER)[EVENT]                            # Fire repeatedly  
if(TRIGGER)((CONDITION))[EVENT]                 # Fire once, conditional
when(TRIGGER)((CONDITION))[EVENT]               # Fire repeatedly, conditional
if(TRIGGER)((CONDITION))[TRUEEVENT][FALSEEVENT] # Fire once, both branches
when(TRIGGER)((CONDITION))[TRUEEVENT][FALSEEVENT] # Fire repeatedly, both branches
```

### Event Chain Syntax
```mms
myChain::;                              # Chain declaration (no semicolon)
event1;                                 # Event with semicolon
((condition))event2;                    # Conditional event
((condition))[trueevent][falseevent];   # Both branches
                                        # Blank line ends chain
```

### Variable Syntax
```mms
# TOP LEVEL - Declarations only (no semicolons)
int myVar=5
bool flag=true
string msg="Hello"

# EVENT CHAINS - Assignments only (with semicolons)  
myChain::;
myVar=10;
flag=false;
```

### Critical Errors (These Break Everything!)
```mms
# ❌ WRONG
if(time:60)[win];                       # Semicolon kills trigger
((health+stamina>100))event;            # Complex expressions not allowed
myVar=10;                               # Assignment at top level

# ✅ CORRECT  
if(time:60)[win]                        # No semicolon on trigger
((totalHealth>100))event;               # Calculate totalHealth separately first
# Assignment in event chain:
init::;
myVar=10;                               # Inside event chain
```

## Variable Types
```mms
# Basic Types
bool flag=true
int count=5  
float value=2.5
string text="Hello"
intarray myArray

# Object References (reference existing objects)
miner bob=0              # References miner ID 0
vehicle truck=1          # References vehicle ID 1
building hq=5,10         # References building at row 5, col 10
```

## Common Triggers
```mms
# Time and tile triggers
if(time:60)[event]              # After 60 seconds
when(drill:5,10)[event]         # When tile drilled
when(enter:5,10)[event]         # When object enters tile
when(click:5,10)[event]         # When tile clicked
```

## Essential Events
```mms
# Game control
win:"Message"           # Win level
lose:"Message"          # Lose level  
msg:"Text"             # Show message

# Tile modification
place:ROW,COL,TILEID   # Place tile (1=ground, 30=rock, 42=crystals)
drill:ROW,COL          # Drill tile

# Object control
heal:OBJECT,AMOUNT     # Heal object
kill:OBJECT           # Remove object
```

## Coordinates
- **Always row,col (Y,X)** - NOT x,y!
- **Count from tiles{} grid** starting at row 0, col 0
- **Never use file line numbers** for coordinates
- **Verify bounds**: row < rowcount, col < colcount

## Common Patterns
```mms
# State tracking
bool gameStarted=false
int stage=0

init::;
gameStarted=true;
stage=1;

# Multi-location triggers  
if(enter:5,10)[safetyCheck]
if(enter:5,11)[safetyCheck] 
if(enter:5,12)[safetyCheck]

# Progressive stages
when(crystals>=10)((stage==1))[advanceToStage2]
```

## Critical Limitations
- **No complex expressions**: `((a+b>10))` → split into separate operations
- **No nested conditions**: `((a>5))((b>3))` → use separate event chains  
- **No variables in triggers**: `if(time:myVar)` → use literal values only
- **No arithmetic in parameters**: `place:row+1,col,5` → calculate first
- **Semicolons kill triggers**: `if(condition)[event];` breaks everything

## Most Common Errors
1. Adding semicolons to triggers
2. Missing square brackets on triggers
3. Spaces after semicolons in chains
4. Using file line numbers for coordinates
5. Complex expressions in conditions

## Key Tile IDs
```mms
# Floors (allow movement)
1   - Ground
6   - Lava  
11  - Water

# Walls (block movement, use regular variants)  
26  - Dirt wall
30  - Loose rock wall
34  - Hard rock wall
38  - Solid rock wall (indestructible)

# Resource seams
42  - Crystal seam
46  - Ore seam  
50  - Recharge seam (air)
```

## Example Script Template
```mms
# Variable declarations at top level (no semicolons)
bool gameStarted=false
int score=0
miner player=0

# Special initialization event chain
init::;
gameStarted=true;
msg:"Game started!";

# Example triggers (no semicolons, square brackets)
if(time:30)[timeWarning]
when(crystals>=10)[checkWin]
when(enter:5,10,player)[playerEntered]

# Event chains (semicolons on events, blank line ends)
timeWarning::;
msg:"30 seconds elapsed";

checkWin::;
((score>=100))[win:"Victory!"][msg:"Keep collecting!"];

playerEntered::;
score+=10;
msg:"Score increased!";
```