# Notes for Py2SCL

### Directories of interest
`$SC2PATH` environmental variable may be present, it contains the path to the Starcraft2 directory.
`$SC2PATH/Maps` directory containing all available maps.
`$SC2PATH/Replays` directory containing all available replays.


#### Source code
If Py2SC was downloaded using this script, the Py2SC source code resides in: 

```bash
~/.local/share/virtualenvs/sc2l_setup-{ENV-ID}/lib/python3.6/site-packages/pysc2/env/
```
Where `{Env-ID}` is randomly generated via virualenv.

### Useful commands
List of all maps: `python -m pysc2.bin.map_list`  
List of all available actions' `python -m python -m pysc2.bin.valid_actions`  
Watch a replay: `python -m pysc2.bin.play --replay <path-to-replay>`  


### Maps
[Ladder maps](http://wiki.teamliquid.net/starcraft2/Maps/Ladder_Maps/Legacy_of_the_Void "Ladder Maps in Legacy of The Void") are maps played by human players on Battle.net. A few are active at a time. Every fewmonths a new season brings a new set of maps.
Melee maps are made specifically for machine learning. The Flat maps have no special features on the terrain, encouraging easy attacking. The number specifies the map size.
The Simple maps are more normal with expansions, ramps, and lanes of attack, but are smaller than normal ladder maps. The number specifies the map size.


## Links of interest:
[PySC2 environment documentation](https://github.com/deepmind/pysc2/blob/master/docs/environment.md "pysc2 environment official documentation")  
[PySC2 Mini-Games documentation](https://github.com/deepmind/pysc2/blob/master/docs/mini_games.md "pysc2 environment official documentation")   
[PySC2 Maps documentation](https://github.com/deepmind/pysc2/blob/master/docs/maps.md "Maps documentation")   
[PySC2 repository](https://github.com/deepmind/pysc2 "PySC2 official repository")  
