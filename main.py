from timetable import TimeTable, options
from numpy.random import rand, randint, shuffle
import matplotlib.pyplot as plt 

POP_SIZE = 2000
ITERATIONS = 200
MUTATION_RATE = 0.2
TASKS_CNT = 80

MIN_DUR = 3
MAX_DUR = 9

def generate(durations):
    tasks = []
    for i, dur in enumerate(durations):
        tasks.append(
            (i, dur, randint(len(options)-1))
        )
    shuffle(tasks)
    return TimeTable(tasks)

def selection(pop, scores, k=3):
    selection_ix = randint(len(pop)-1)
    for ix in randint(0, len(pop), k-1):
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

def getBest(pop):
    best = pop[0]
    bestms = pop[0].makespan()
    for t in pop:
        ms = t.makespan()
        if ms<bestms:
            bestms=ms
            best = t
    return best

durations = [randint(MIN_DUR, MAX_DUR) for _ in range(TASKS_CNT)]

print("sum of durations",sum(durations))

pop = [generate(durations) for _ in range(POP_SIZE)]

makespanHistory = []

scores = [t.makespan() for t in pop]
print("initial best score = ",min(scores))
makespanHistory.append(min(scores))
bestSolution = getBest(pop)

for it in range(ITERATIONS):
    
    new_pop = []
    
    for i in range(int(POP_SIZE/2)):
        
        p1, p2 = selection(pop, scores), selection(pop, scores)
        
        c1, c2 = p1.order_crossover(p2)

        if rand()<MUTATION_RATE: c1.mutate()
        if rand()<MUTATION_RATE: c2.mutate()
        
        new_pop.append(c1)
        new_pop.append(c2)
        
    pop = new_pop
    
    scores = [t.makespan() for t in pop]
    print("iteration ",it+1," best score = ",min(scores))
    makespanHistory.append(min(scores))
    bestIterSolution = getBest(pop)
    if bestSolution.makespan() > bestIterSolution.makespan():
        bestSolution = bestIterSolution
    

print("--------------------")
bestSolution.printColor()
print("--------------------")
# bestSolution.printAscii()
# print("--------------------")
print("best makespan = ",bestSolution.makespan())

plt.plot(range(len(makespanHistory)), makespanHistory) 
plt.xlabel('iterations') 
plt.ylabel('makespan') 
plt.show() 
