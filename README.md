# Blandrice's Library

📖☕ Hi Friends, welcome to my library ☕📖

I made a quick script to do Krunkscript Library. I'm hoping it makes scripting easier for now

<p align="center">
  <img src="docs/blandlib.png" />
</p>

# How it Works
1. Including: 
    - C-style syntax is used : `#include <lib.krnk>`
2. Process: 
    - Search-Replace: will happen for libraries in the above `#include` path 
        - import happens once per library (cannot import library 2 times)
    - Global Variables and Actions: wil be prepended with library name
        - e.g. in `lib.krnk`, 
            - global var `num time` --> `num lib_time`
            - global action `num action myaction()` --> `num action lib_myaction()`
    - Recursion: Libraries can include other Libraries (again, cannot include more than once)
        - e.g. `lib.krnk` can have `#include <other_lib.krnk>`
            - be careful - the global variables will keep prepending (in above example: `num lib_other_lib_time`)

    - A library's **public actions** are automatically inserted/prepended, e.g.:
        
            public action start(){
                library_start(); # <-- automatically added 
                # your script's start code
                ...
            }
            
3. Invoking:
    
        python py/compile.py maps/testmap_client.krnk

    output will be printed in the `/out` folder

# Library Example!!

Example HEADER:

https://github.com/blandrice/blandlibs/blob/master/libs/doublejump/DJ_head.krnk

```cs
# ===================================================================
# Header: doublejump\DJ_head.krnk
# Author: blandrice
# ===================================================================

# ===================================================================
# SETTINGS:
num MAX_JUMPCOUNT = 2; # 2 is "doublejump", 3 is "triplejump"
bool WALLJUMP_REFRESHS = true;
bool ENABLE_CROUCHJUMP = true; # lower height for crouch jump, also
                                # applies "moonjump" mid-air physics
num SOUND = 31960; # sound ID. set to 0 if no sound desired

# HARD-CODED NUMBERS - DON'T TOUCH
num MS_DURATION_UNCROUCH = 166;
num HEIGHT_JUMP = 0.0793; # 60FPS, max clearance 17.9 units
num HEIGHT_CROUCHJUMP = 0.0595; # 60FPS, max clearance 10.2 units
# ===================================================================
```

Example LIBRARY: (calls header)

https://github.com/blandrice/blandlibs/blob/master/libs/doublejump/djump_client.krnk

```cs
#include <DJ_head.krnk>

# ===================================================================
# Library: doublejump\djump_client.krnk
# Author: blandrice
# ===================================================================

obj updateState = { updateId: 0, playerUpdateId: 0, lastUpdate: 0 };
obj currentPlayerState = {};
obj[] playerStateHistory = obj[];

obj action findHistoryState() {
    # Current state that was synced up was the last state
    obj currentState = playerStateHistory[lengthOf playerStateHistory - 1];
    obj[] possibleStates = obj[];
    num highestMatches = 0;


# .........more code...
```

Example MAP SCRIPT (calls library):

https://github.com/blandrice/blandlibs/blob/master/maps/test_djump/testdjump_client.krnk

```cs
#include <djump_client.krnk>

# ===================================================================
# File: maps/test_djump/testdjump_client.krnk
# Author: blandrice
# ===================================================================

num map_var = 0;

public action start()
{
    # nothing to see here
}
```

Example OUTPUT SCRIPT:

https://github.com/blandrice/blandlibs/blob/master/out/o_testdjump_client.krnk

```cs
# ===================================================================
# Header: doublejump\DJ_head.krnk
# Author: blandrice
# ===================================================================

# ===================================================================
# SETTINGS:
num djump_client_DJ_head_MAX_JUMPCOUNT = 2; # 2 is "doublejump", 3 is "triplejump"
bool djump_client_DJ_head_WALLJUMP_REFRESHS = true;
bool djump_client_DJ_head_ENABLE_CROUCHJUMP = true; # lower height for crouch jump, also
                                # applies "moonjump" mid-air physics
num djump_client_DJ_head_SOUND = 31960; # sound ID. set to 0 if no sound desired

# HARD-CODED NUMBERS - DON'T TOUCH
num djump_client_DJ_head_MS_DURATION_UNCROUCH = 166;
num djump_client_DJ_head_HEIGHT_JUMP = 0.0793; # 60FPS, max clearance 17.9 units
num djump_client_DJ_head_HEIGHT_CROUCHJUMP = 0.0595; # 60FPS, max clearance 10.2 units
# ===================================================================
# ===================================================================
# Library: doublejump\djump_client.krnk
# Author: blandrice
# ===================================================================

obj djump_client_updateState = { updateId: 0, playerUpdateId: 0, lastUpdate: 0 };
obj djump_client_currentPlayerState = {};
obj[] djump_client_playerStateHistory = obj[];

obj action djump_client_findHistoryState() {
    # Current state that was synced up was the last state
    obj currentState = djump_client_playerStateHistory[lengthOf djump_client_playerStateHistory - 1];
    obj[] possibleStates = obj[];
    num highestMatches = 0;

    # check all 6 position/velocity number

# .... more code ...

# ===================================================================
# File: maps/test_djump/testdjump_client.krnk
# Author: blandrice
# ===================================================================

num map_var = 0;

public action start () {
{
    # nothing to see here
}}

# ================================================================
# auto-detected public actions from libraries
# ================================================================
public action onPlayerSpawn (str id) {
    djump_client_onPlayerSpawn(id);
}

public action update (num delta) {
    djump_client_update(delta);
}

public action onPlayerUpdate (str id, num delta, obj inputs) {
    djump_client_onPlayerUpdate(id,  delta,  inputs);
}


```

# Directory Structure
`/libs`: use/put your libraries here

`/maps`: Create your map scripts (client/server side) here

`/out`: final compiled output script here

Example Structure:

    \BLANDLIBS
    ├───libs # 1. all libraries referenced will be here
    │   │   raybox.krnk
    │   │
    │   └───float16
    │           float16.krnk
    │
    ├───maps # 2. create your mapfile here (including libraries above)
    │       testmap_client.krnk # calls raybox.krnk, float16.krnk
    │
    ├───out # 4. compiled map file (put this into KrunkScript editor)
    │       testmap_client.krnk
    │
    ├───py # 3. python file to be called
    │       compile.py
    │
    └───temp # scratch space for compile.py

# Example Library Import

    #include <raybox.krnk> 
    #include <float16.krnk>

# How to Invoke Library Compiler

    cd blandlibs
    python py/compile.py maps/testmap_client.krnk


# Notes
My parsing is not the best because this is just a quick job to get libs before Krunker actually implements them!

Watch out for these bad practices that may break my code:
- do NOT include brackets () in `# comments`
- do NOT MANUALLY include calls to update functions in other libraries in any script
    - My python script should handle that for you
- do NOT mess with the syntax of public action line too much
    - e.g. `public action update(num delta) {`
        - best just to keep it in one line like a normal person would
- I am not responsible for conflicting libraries e.g.:
    - sendNetworkMessage() limit exceeded
    - onPlayerUpdate player position/velocity conflicts