# Blandrice's Library
<center>📖☕ Hi Friends, welcome to my library ☕📖</center>
<center>I made a quick script to do Krunkscript Library. I'm hoping it makes scripting easier for now!</center>



<p align="center">
  <img src="docs/blandlib.png" />
</p>

1.  C-style syntax is used : `#include <lib.krnk>`
2. Libraries insert only once 
    - (for those familiar with C, that means there is no need to guard using `#ifdef`)
3. A library's **public actions** are automatically inserted/prepended, e.g.:
    
        public action start(){
            library_start(); # <-- automatically added 
            # your script's start code
            ...
        }
        

Here's some more details:


# Directory Structure
`\libs`: use/put your libraries here

`\maps`: Create your map scripts (client/server side) here

Example Structure:

    \BLANDLIBS
    ├───libs # all libraries referenced will be here
    │   │   raybox.krnk
    │   │
    │   └───float16
    │           float16.krnk
    │
    ├───maps # create your mapfile here (including libraries above)
    │       testmap_client.krnk # calls raybox.krnk, float16.krnk
    │
    ├───out # compiled map file (put this into KrunkScript editor)
    │       testmap_client.krnk
    │
    ├───py # python file to be called
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
- do not include brackets () in `# comments`
- do NOT MANUALLY include calls to update functions in other libraries in any script
    - My python script should handle that for you
- don't mess with the syntax of public action line too much
    - e.g. `public action update(num delta) {`
        - best just to keep it in one line like a normal person would