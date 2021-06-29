import gym;
import eplus_env;

env = gym.make('Eplus-test-v4');
curSimTime, ob, isTerminal = env.reset(); # Reset the env (creat the EnergyPlus subprocess)
while not isTerminal:
    action = [-30, -30];
    print(ob[8])
    curSimTime, ob, isTerminal = env.step(action);
env.end_env(); # Safe termination of the environment after use.
