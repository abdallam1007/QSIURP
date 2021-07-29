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

max_energy = 11000
min_energy = 0
max_temp = 24
min_temp = 0


def normalize(x,x_max,x_min):

  if x < x_min:
    x = x_min
  elif x > x_max:
    x = x_max

  return (x_max - x) / (x_max - x_min)

def cubic(x, scale = - 0.1, translation = 0):
  return translation + (x**3) * scale

def getReward(sp,rt,E15):
  a = 0.5
  delta_sp = abs(sp - rt)
  norm_e = normalize(E15,max_energy,min_energy)
  norm_t = normalize(delta_sp,max_temp,min_temp)
  R = a * norm_e + (1-a) * norm_t
  return cubic(8 * R - 4, scale = -0.1, translation = 2)

def simulate(sp,inTemps,outTemps):
  alpha = 0.6
  gamma = 0.9
  epsilon = 0.1

  # making the initial Q-table
  qTable = getQTable(inTemps,outTemps)
  
  #freqTable = getFreqTable(inTemps,outTemps)
  env = gym.make('Eplus-test-v4')

  cum_R_List = []

  # Number of episodes
  for i in range(1):
    cum_R = 0

    # Reset the env (creat the EnergyPlus subprocess)
    curSimTime, ob, isTerminal = env.reset()
    
    # get the initial in/out temps and the energy consumption
    state = (round(ob[8]),round(ob[0]))
    energyC = ob[14] # ???
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
      cum_R += reward

      oldQValue = qTable[state][choice]
      nextQMax = max(qTable[nextState])
      # update the Q - Value
      newQValue = oldQValue + alpha * (reward + gamma * nextQMax - oldQValue)
      qTable[state][choice] = newQValue
      # ble ate ice
      #freqTable[state] += 1

      state = nextState
      # ate next ate (زي المفجوع)
    cum_R_List.append(cum_R)

  #plt.plot(cum_R_List)

# Safe termination of the environment after use.
  env.end_env()

simulate(30,(0,31),(-17,35))

# u late i u ate


# plot learning rate