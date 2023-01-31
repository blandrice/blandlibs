# Moving Platforms using Path Nodes
You can have krunkscript find all the path nodes in a map.
I used it to spawn in moving platforms

https://streamable.com/7gu4gq

https://streamable.com/qu3148

Try it here:
https://krunker.io/social.html?p=map&q=DJ_BlueCove

## Editor View
![editor](editor.png)

## In-Game View
![ingame](ingame.png)

## How to use

1. import plats_test_save.txt (the krunkscripts are already saved)
2. move groups of platforms around to place them
3. to make new platforms, you MUST update the path node ID to a different value (each platform **MUST** have a unique path node ID values)

## Path Node ID's
To access a different direction of moving platform, you must use an ID within the range specified. use the server krunkcript / or definitions below to help you choose the ID number. There are signs on the template map to tell you which platform it is.

        # pathnode ID ranges for back and forth linear platforms
        num N_X_LIN_PLATSTART        =  0;
        num N_X_LIN_PLATEND          = 50;

        num N_X_LIN_0_5_PLATSTART    =  51;
        num N_X_LIN_0_5_PLATEND      = 100;

        num N_Y_LIN_PLATSTART        = 101;
        num N_Y_LIN_PLATEND          = 150;

        num N_Y_LIN_0_5_PLATSTART    = 151;
        num N_Y_LIN_0_5_PLATEND      = 200;

        num N_Z_LIN_PLATSTART        = 201;
        num N_Z_LIN_PLATEND          = 250;

        num N_Z_LIN_0_5_PLATSTART    = 251;
        num N_Z_LIN_0_5_PLATEND      = 300;

        num N_VERT_CIRCLEX_PLATSTART = 301;
        num N_VERT_CIRCLEX_PLATEND   = 350;

        num N_VERT_CIRCLEX_0_5_PLATSTART = 351;
        num N_VERT_CIRCLEX_0_5_PLATEND   = 400;

        # 701-800
        num N_VERT_CIRCLEX_CC_PLATSTART = 701;
        num N_VERT_CIRCLEX_CC_PLATEND   = 750;

        num N_VERT_CIRCLEX_CC_0_5_PLATSTART = 751;
        num N_VERT_CIRCLEX_CC_0_5_PLATEND   = 800;
        # 701-800

        num N_VERT_CIRCLEZ_PLATSTART = 401;
        num N_VERT_CIRCLEZ_PLATEND   = 450;

        num N_VERT_CIRCLEZ_0_5_PLATSTART = 451;
        num N_VERT_CIRCLEZ_0_5_PLATEND   = 500;

        # 801-900
        num N_VERT_CIRCLEZ_CC_PLATSTART = 801;
        num N_VERT_CIRCLEZ_CC_PLATEND   = 850;

        num N_VERT_CIRCLEZ_CC_0_5_PLATSTART = 851;
        num N_VERT_CIRCLEZ_CC_0_5_PLATEND   = 900;
        # 801-900


        num N_HOR_CIRCLE_PLATSTART   = 501;
        num N_HOR_CIRCLE_PLATEND     = 550;

        num N_HOR_CIRCLE_0_5_PLATSTART   = 551;
        num N_HOR_CIRCLE_0_5_PLATEND     = 600;

        num N_HOR_CIRCLE_CC_PLATSTART   = 601;
        num N_HOR_CIRCLE_CC_PLATEND     = 650;

        num N_HOR_CIRCLE_0_5_CC_PLATSTART   = 651;
        num N_HOR_CIRCLE_0_5_CC_PLATEND     = 700;
## Known issues
1. player behavior is disabled to make platforms work which  means
        
    - score zones wont work
    - death zones wont work 
    - speedrun timers wont work