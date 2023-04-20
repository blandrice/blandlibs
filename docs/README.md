# Blandrice's Library

📖☕ Hi friends, welcome to my library ☕📖

I made a quick script to do Krunkscript Library. I'm hoping it makes scripting easier and more portable for now.

This is just a quick job to get some sort of library feature before Krunker actually implements the official version, and so I can start packaging my own libraries. But hopefully it is useful to other KrunkScripters 😊

<p align="center">
  <img src="blandlib.png" />
</p>


# Library Example!

[Example HEADER](/libs/doublejump/DJ_head.krnk) --> [Example LIBRARY](/libs/doublejump/djump_client.krnk) --> [Example MAP SCRIPT](/libs/doublejump/test/testdjump_client.krnk) --> [Example FINAL SCRIPT](/out/o_testdjump_client.krnk)


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
    - Recursion: Libraries can include other Libraries (AKA headers) (again, cannot include more than once)
        - e.g. `lib.krnk` can have `#include <other_lib.krnk>`

    - A library's **public actions** are automatically inserted/prepended, e.g.:
        
            public action start(){
                library_start(); # <-- automatically added 
                # your script's start code
                ...
            }
            
3. Invoking:
    
        python py/compile.py maps/testmap_client.krnk

    output will be printed in the `/out` folder




# Directory Structure
`/libs`: use/put your libraries here

`/maps`: Create your map scripts (client/server side) here

`/out`: final compiled output script here

Example Structure:

    \BLANDLIBS
    ├───libs # 1. add libraries here
    │   └───doublejump 
    │           djump_client.krnk
    │           djump_server.krnk
    │           DJ_head.krnk
    │
    ├───maps # 2. create map scripts (call libraries) here
    │   └───test_djump
    │           testdjump_client.krnk
    │           testdjump_server.krnk
    │
    ├───out # 4. final output script here goes into krunker editor
    │       o_testdjump_client.krnk
    │
    ├───py # 3. run compile script on maps/script.krnk
    │       compile.py

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
- do NOT MANUALLY include calls to public actions in other libraries in any script
    - My python script should handle that for you
- do NOT mess with the syntax of public action line too much
    - e.g. `public action update(num delta) {`
        - best just to keep it in one line like a normal person would
- I am not responsible for conflicting libraries e.g.:
    - sendNetworkMessage() limit exceeded
    - onPlayerUpdate player position/velocity conflicts