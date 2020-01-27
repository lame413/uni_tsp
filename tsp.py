#!/usr/bin/python

from random import shuffle, randint, random
import os

adaptiveMutation = True
debug = False

def tournament(scores, tournamentSize):
  # getting X random individuals into the tournament
  tmpRange = list(range(0, len(scores)))
  shuffle(tmpRange)
  rng = tmpRange[:int(tournamentSize)]

  # get best members as parents
  p1 = min(rng, key=lambda idx: scores[idx])
  del rng[rng.index(p1)]
  p2 = min(rng, key=lambda idx: scores[idx])

  return (p1,p2)

def roulette(scores):
  # get worst distance
  worst = max(scores)
  max_minus_scores = scores.copy()

  # calculate roulette scores
  for idx, i in enumerate(max_minus_scores):
    if max_minus_scores[idx] == worst:
      max_minus_scores[idx] = 1
    else:
      max_minus_scores[idx] = worst - max_minus_scores[idx] + 1
  total = sum(max_minus_scores)

  # calculate selection tresholds 
  roulette_selection_tresholds = []*len(max_minus_scores)
  for idx, i in enumerate(max_minus_scores):
    roulette_selection_tresholds.append('')
    if(idx == 0):
      roulette_selection_tresholds[idx] = i
    else:
      roulette_selection_tresholds[idx] = roulette_selection_tresholds[idx-1] + i

  # select the first parent
  p1 = -1
  p2 = -1
  while p1 == -1 or p2 == -1:
    l = randint(1, total)
    for idx, i in enumerate(roulette_selection_tresholds):
      if(l > i):
        continue
      else:
        if p1 == -1:
          p1 = idx

        # check for repeats, so that the parents aren't identical
        if p1 == idx:
          break
        else:
          p2 = idx
        break 

  return (p1, p2)

# first population
def genPaths(paths, nc):
  population = []   
  for i in range(paths):
    population.append(list(range(nc)))
    shuffle(population[i])
  return population

def debugPathLength(path, pathScore):
  for idx, x in enumerate(path):
    if(idx != len(path)-1):
      print(x, '-', sep='', end='')
    else:
      print(x, pathScore)

def calculateDistances(population, listOfDistances):
  pathDistances = []
  for i in population:
    tmpDist = 0
    for j in range(len(population[0])):
      if j-1 < len(population[0]):
        tmpDist += int(listOfDistances[ i[j-1] ] [ i[j] ])
      else:
        print("added last path")
        tmpDist += int(listOfDistances[ i[j-1] ] [ i[0] ])
    pathDistances.append(tmpDist)
  return pathDistances

def permutate(c1, c2):
  # get the range of genes to copy over
  segment_start = 0
  segment_end = len(c1)

  while(segment_start + segment_end == len(c1) 
    or abs(segment_start - segment_end) <= 2):
    segment_start = randint(0, len(c1))
    segment_end = randint(0, len(c2))

  if(segment_start > segment_end):
    segment_start, segment_end = segment_end, segment_start
  
  # copy over the genes from parent 1
  child = ['']*(segment_start)
  for i in range(segment_start, segment_end):
    child.append(c1[i])
  child.extend(['']*(len(c1)-segment_end))
   
  # pmx 
  for i in range(segment_start, segment_end):
    if c2[i] in child:
      continue

    # take care of collisions in the 
    # copied over bit of the child's genome 
    curVal = c2[i]
    tmpVal = c2[i]
    indexTmp = ''
    while True:
      tmpVal = c1[c2.index(tmpVal)]
      indexTmp = c2.index(tmpVal)
      if indexTmp in range(segment_start, segment_end):
        tmpVal = c2[indexTmp]
        continue
      child[indexTmp] = curVal
      break
  
  # copy over the rest of c2 to the child
  for idx, i in enumerate(child):
    if child[idx] == '':
      child[idx] = c2[idx]

  return child

def mutate(path):
  c1 = randint(0, len(path)-1)
  c2 = randint(0, len(path)-1)

  while c1 == c2: 
    c2 = randint(0, len(path)-1)

  path[c1], path[c2] = path[c2], path[c1]
  return path

print("Select the file to work with: ")

files = os.listdir("./lists")
for idx, i in enumerate(files):
  print(idx+1, ") ", i, sep='')
print("---- quick presets ----")
print("r) quick roulette (berlin, 5000 gens, pop size 30, adaptive mutation)")
print("t) quick tournament (berlin, 5000 gens, pop size 30, adaptive mutation)")
print("q) quit")

choice = input()
if choice.isnumeric() != True:
  if choice == 'r' or choice == 't':
    selectedFile = "berlin52.txt"
  else:
    quit()
elif int(choice) not in range(0, len(files)+3):
  quit()
else:
  selectedFile = files[int(choice)-1]

if choice == 'r' or choice == 't':
  nPaths = 30
else:
  nPaths = int(input("Size of population? (even):"))
if (nPaths % 2 != 0):
  nPaths = nPaths + 1
  print("Adjusted size of population to", nPaths)

if choice == 'r' or choice == 't':
  maxGen = 5000 
else:
  maxGen = int(input("Maximum number of generations?"))
#maxStagnation = 1000 # int(input("Maximum number of generations with no improvement?"))

mutationChance = 0.01
if choice == 'r' or choice == 't':
  adaptiveMutation = True
else:
  adaptiveMutationTmp = input("Adaptive mutation? (increases with generation, Y/N):")
  if adaptiveMutationTmp.upper() == 'Y':
    adaptiveMutation = True
  if adaptiveMutationTmp.upper() == 'N':
    adaptiveMutation = False
    mutationChanceTmp =  input ("Chance to mutate? (default: 0.01):")
    if len(mutationChanceTmp) != 0:
      mutationChance = float(mutationChanceTmp) 

if choice == 'r':
  selection = 2
elif choice == 't':
  selection = 1
else:
  print("Tournament or roulette?")
  print("1) Tournament")
  print("2) Roulette")
  selection = int(input())

if selection == 1:
  tournamentSize = input("Tournament size?:")
elif selection != 2:
  print("Wrong input")
  quit()

# loading the list and splitting it into a 2d array  
f = open("./lists/" + selectedFile, "r")
fl = f.readlines()

# nc - Number of Cities
nc = int(fl[0])
lr = fl[1:]
listOfDistances = []
for i in lr:
  tmp = i.split(' ')
  listOfDistances.append(tmp[:-1])

# mirroring the array 
for i in range(int(nc)):
  for j in range(i+1, int(nc)):
    listOfDistances[i].append(listOfDistances[j][i])

# generate random paths
population = genPaths(nPaths, nc)

generation = 0
bestPath = (-1, -1)
newPop = population.copy()
parents = ''
stagnation = 0

while generation < maxGen: #and stagnation < maxStagnation:
  oldPop = newPop.copy()
  newPop = []

  # calculate distances, save to scores
  scores = calculateDistances(oldPop, listOfDistances)
  best = min(scores)

  # get best path from current generation
  tmpBestPath = (best, oldPop[scores.index(best)])

  # swap if better than best overall
  if generation == 0 or tmpBestPath[0] < bestPath[0]:
    stagnation = 0
    bestPath = tmpBestPath

  # stagnation = stagnation + 1

  if selection == 1:
    tmpPop = oldPop.copy()

  # generate next generation
  while len(newPop) < len(oldPop):
    if selection == 1:
      parents = tournament(scores, tournamentSize)
    if selection == 2:
      parents = roulette(scores)

    parent1 = oldPop[parents[0]]
    parent2 = oldPop[parents[1]]

    newPop.append(permutate(parent1, parent2))

    # testing adaptive mutation
    if adaptiveMutation:
      mutationChance = (1-((maxGen-generation)/maxGen))/10

    if random() < mutationChance:
      newPop[-1] = mutate(newPop[-1])

  if len(population) > 200 or generation % 50 == 0:
    print("Generation ", generation, ", best path so far: ", bestPath[0], sep='')
    if adaptiveMutation:
      print("Current mutation chance:", mutationChance)

  generation = generation + 1

print("Done! Generations: ", generation, ", best path: ", bestPath[0], sep='')
print()
print("Path itself:")
#print(bestPath[1])

debugPathLength(bestPath[1], bestPath[0])
