# Notes for Py2SCL

### Requirements

The script is meant to be used in LINUX distributions.   
The installation script uses [pipenv](https://docs.pipenv.org/ "pipenv tutorial") to handle python virtual environments. If you don't have `pipenv` installed in your system you can use `pip install pipenv` to install it.

Once `pipenv` is installed, run this command inside the directory to install all required dependencies: `pipenv install`. For more information regarding `pipenv`, run `pipenv` (the commands without argument).


### Installation script

The installation follows these steps:  
1. Checks if StarcraftII is already installed. It downloads it and installs it otherwise.   
2. Downloads all available maps listed in the map section [here](https://github.com/Blizzard/s2client-proto "StarcraftII client protocol").      
3. Downloads all available replays found in the replays section [here](https://github.com/Blizzard/s2client-proto "StarcraftII client protocol").   

### Troubleshooting 

Firstly, be a smart cookie. This script has worked on various machines, any installation error will most likely be due to some dependency missing on your system. Try to see what dependency it is and install it.

`box2d-kengz` depends on [swig](www.swig.org). Swig can be installed on the command line via `sudo apt-get install swig`



### Directories of interest
`$SC2PATH` environmental variable may be present, it contains the path to the Starcraft2 directory.  
`$SC2PATH/Maps` directory containing all available maps.  
`$SC2PATH/Replays` directory containing all available replays.  

 StarCraftII directory structure:  
 ```bash
    StarCraft II/
        Battle.net/
        Maps/
        Replays/
        SC2Data/
        Versions/
 ```


#### Source code
If Py2SC was downloaded using this script, the Py2SC source code resides in: 

```bash
~/.local/share/virtualenvs/sc2l_setup-{ENV-ID}/lib/python3.6/site-packages/pysc2
```
Where `{Env-ID}` is randomly generated via pipenv.

### Useful commands
List of all maps: `python -m pysc2.bin.map_list`  
List of all available actions' `python -m pysc2.bin.valid_actions`  
Watch a replay: `python -m pysc2.bin.play --replay <path-to-replay>`  

In case you are not familiar with the `-m` flag (module-name flag), an extract from the `man python` documention:
```
-m module-name
              Searches sys.path for the named module and runs the corresponding .py file as a script.
```



### Maps
[Ladder maps](http://wiki.teamliquid.net/starcraft2/Maps/Ladder_Maps/Legacy_of_the_Void "Ladder Maps in Legacy of The Void") are maps played by human players on Battle.net. A few are active at a time. Every fewmonths a new season brings a new set of maps.  
Melee maps are made specifically for machine learning. The Flat maps have no special features on the terrain, encouraging easy attacking. The number specifies the map size.
The Simple maps are more normal with expansions, ramps, and lanes of attack, but are smaller than normal ladder maps. The number specifies the map size.


## Links of interest:
[PySC2 environment documentation](https://github.com/deepmind/pysc2/blob/master/docs/environment.md "pysc2 environment official documentation")  
[PySC2 Mini-Games documentation](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md "pysc2 environment official documentation")   
[PySC2 Maps documentation](https://github.com/deepmind/pysc2/blob/master/docs/maps.md "Maps documentation")   
[PySC2 repository](https://github.com/deepmind/pysc2 "PySC2 official repository")   
[Blizzard Starcraft II client repository](https://github.com/Blizzard/s2client-proto "Blizzard StarcraftII client repository")  
[DeepMind StarCraft II Paper](https://deepmind.com/documents/110/sc2le.pdf "PDF version of StarCraft II paper")  
