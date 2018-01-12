import pysc2.maps import lib

""" 
    In order to add this set of maps into pysc2, we need to do 2 things:
    1: modify __init__.py in pysc2/maps/ and add the following line
        from pysc2.maps import first_experiment
    2: copy this script into pysc2/maps/
"""

class FirstExperiment(lib.Map):
    """ Name of the Class: name of the group of maps 
        Note how FirstExperiment inherits from lib.Map
        directory names the directory under StarcraftII/Maps/ which hosts the maps named below
    """

    directory = "FirstExperiment"
    download  = None
    players   = 1
    game_steps_per_episode = 16 * 60 * 5 # 5 minutes per episode
    score_index = 0 

first_experiment_maps = [
    "marine-vs-zerglings"
]

for name in first_experiment_maps:
    globals()[name] = type(name, (FirstExperiment,), dict(filename=name))
