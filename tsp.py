from random import shuffle, randint

def genPaths(nc):
  rngPaths = []   
  for i in range(nc):
    rngPaths.append(list(range(nc)))
    shuffle(rngPaths[i])
  return rngPaths

def calculateDistances(rngPaths, nc, lm):
  pathDistances = []
  for idx, i in enumerate(rngPaths):
    tmpDist = 0
    for j in range(nc-1):
      if j < nc-1:
        tmpDist += int(lm[ i[j] ] [ i[j+1] ])
      else:
        tmpDist += int(lm[ i[j] ] [ i[0] ])
    print("path", idx+1, "out of", len(rngPaths), " = ", tmpDist)
    pathDistances.append(tmpDist)
  return pathDistances
  

#f = open("berlin52.txt", "r")
#fl = f.readlines()
# loading the list and splitting it into a 2d array
lr = list(fl.split('\n'))
nc = int(lr[0])
lr = lr[1:]
lm = []
for i in lr:
    tmp = i.split(' ')
    if tmp[-1] == '':
      lm.append(tmp[:-1])
    else:
      lm.append(tmp)

# mirroring the array
for i in range(int(nc)):
  for j in range(i+1, int(nc)):
    lm[i].append(lm[j][i])

# generating random paths
rngPaths = genPaths(nc)
  
# calculating the distances
scores = calculateDistances(rngPaths, nc, lm)
print(scores)

# get worst score
worst = max(scores)

# roulette'ify the scores
for idx, i in enumerate(scores):
  if scores[idx] == worst:
    scores[idx] = 1
  else:
    scores[idx] = worst - scores[idx] + 1
total = sum(scores)
print(scores)
print(total)

# generate stuff? scores? edges? can't think rn
scores_roulette = []*len(scores)
for idx, i in enumerate(scores):
  scores_roulette.append('')
  if(idx == 0):
    scores_roulette[idx] = i
  else:
    scores_roulette[idx] = scores_roulette[idx-1] + i

scores_tmp = [0]*(len(scores_roulette))
for idx, i in enumerate(scores_roulette):
  l = randint(1, total)
  for idx, i in enumerate(scores_roulette):
    if(l > i):
      continue
    else:
      scores_tmp[idx] += 1
      break

print("paths adjusted to roulette scoring: ", scores)
print("ranges:", scores_roulette)
print("hits per path:", scores_tmp)

scores_sorted = []
for idx, i in enumerate(scores_tmp):
  if(i > 0):
    scores_sorted.append((scores_copy[idx], scores_tmp[idx]))
print(scores_sorted)
    
    
