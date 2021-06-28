## The idf files included: (QSIURP/Gym-Eplus/eplus_env/envs/eplus_models/demo_5z/learning/idf)
- 1SmallRoom.idf        : Contains one room, one door, one window, lights and an ideal HVAC system.
- 1ZoneEvapCooler.idf   : One of the example files that contains one zone with a realistic HVAC system.
- 5ZoneAutoDXVAV_v0.idf : The default five zones file with their realistic HVAC system.
- 1ZoneAutoDXVAV_v0.idf : The default five zones file after being modified to contain only one zone (same as 1SmallRoom.idf) with the same HVAC system as                                     5ZoneAutoDXVAV_v0.idf modidifed for only one room.

## The cfg files included: (QSIURP/Gym-Eplus/eplus_env/envs/eplus_models/demo_5z/learning/cfg)
- 1SmallRoom.cfg        : To be used with 1SmallRoom.idf
- 1ZoneEvapCooler.cfg   : To be used with 1ZoneEvapCooler.idf
- 5ZoneAutoDXVAV_v0.cfg : To be used with 5ZoneAutoDXVAV_v0.idf and 1ZoneAutoDXVAV_v0.idf

## Python Notebooks: (QSIURP/Simulations)
- Testing.ipynb  : A simulation and a plot of the in and out temps for 1ZoneAutoDXVAV_v0.idf
- Testing2.ipynb : A simulation and a plot of the in and out temps for 1ZoneEvapCooler.idf
