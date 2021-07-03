import gym;
import eplus_env;
import random
import statistics

# Input: inTemps  = (r1,r2) where r1,r2 are a range of room temps (0,30)
#        outTemps = (r3,r4) where r3,r4 are a range of out temps (-17,35)
# Output: a dict with the cartesian product of both in and out temps
#         as a key and 0 as a value.
def getQTable(inTemps,outTemps):
  (r1,r2) = inTemps
  (r3,r4) = outTemps
  qList = []
  for i in range(r1,r2):
    for j in range(r3,r4):
        # Making a dict where the states (i,j) are the keys and the value 
        # is an array where the indices represent the actions (0 => off),
        # (1 => on = 30) respectively and the elements of the array are 
        # the Q-Value for each state and action (key and value).
        qList.append(((i,j),[0,0]))
  qDict = dict(qList)
  return qDict

'''
def getFreqTable(inTemps,outTemps):
  (r1,r2) = inTemps
  (r3,r4) = outTemps
  freqList = []
  for i in range(r1,r2):
    for j in range(r3,r4):
        freqList.append(((i,j),0))
  freqDict = dict(freqList)
  return freqDict
'''

def getReward(sp,rt,energy):
  # 128 is the mean value
  return 128 - round(abs(sp - rt) * (energy // 100))

def simulate(sp,inTemps,outTemps):
  alpha = 0.6
  gamma = 0.9
  epsilon = 0.1

  # making the initial Q-table
  qTable = getQTable(inTemps,outTemps)
  
  #freqTable = getFreqTable(inTemps,outTemps)
  env = gym.make('Eplus-test-v4')

  # Number of episodes
  for i in range(10):

    # Reset the env (creat the EnergyPlus subprocess)
    curSimTime, ob, isTerminal = env.reset()
    
    # get the initial in/out temps and the energy consumption
    state = (round(ob[8]),round(ob[0]))
    energyC = ob[14] # ???
    reward = 0
    while not isTerminal:
      if random.uniform(0,1) < epsilon:
        choice = random.randint(0,1)
      else:
        # a list of qValues indexed by actions
        actionsList = qTable[state]
        choice = actionsList.index(max(actionsList))
      
      # (0 = off) (1 = on,30)
      if choice:
        action = [sp,sp]
      else:
        action = [0,0]
      
      curSimTime, ob, isTerminal = env.step(action)
      nextState = (round(ob[8]),round(ob[0]))

      # get the energy consumption for the last 15 mins
      energyC = abs(energyC - ob[14])
      reward = getReward(sp,ob[8],energyC)

      oldQValue = qTable[state][choice]
      nextQMax = max(qTable[nextState])
      # update the Q - Value
      newQValue = oldQValue + alpha * (reward + gamma * nextQMax - oldQValue)
      qTable[state][choice] = newQValue
      # ble ate ice
      #freqTable[state] += 1

      state = nextState
      # ate next ate (زي المفجوع)

# Safe termination of the environment after use.
  env.end_env()

  #maxKey = max(freqTable,key=freqTable.get)
  #print(maxKey,qTable[maxKey])
  #print(qTable)

simulate(30,(0,31),(-17,35))

# u late i u ate