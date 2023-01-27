from termcolor import colored
from numpy.random import randint, rand, shuffle

WORKERS_CNT=5
DAY_LENGTH=18

options = [(a, b) for a in range(WORKERS_CNT) for b in range(WORKERS_CNT) if b>=a]

colors = [
    'on_red','on_green','on_yellow','on_blue','on_magenta','on_cyan',
    'on_light_grey','on_dark_grey','on_light_red','on_light_green',
    'on_light_yellow','on_light_blue','on_light_magenta','on_light_cyan'
]

shuffle(colors)

tablePrintChars = "ABCDEFGHKMNOPRSUXYZ@#$%*"

class TimeTable:
    def __init__(self, tasks):
        self.tasks = tasks
        
    def _toFill(self, until, toadd):
        rem = DAY_LENGTH - until%DAY_LENGTH
        if rem<toadd:
            return rem
        return 0
        
    def makespan(self):
        workers = [0]*WORKERS_CNT
        
        for (_,dur,opt) in self.tasks:
            (a,b) = options[opt]

            if a == b:
                workers[a] += self._toFill(workers[a],dur)
                workers[a] += dur
            else:
                half = int((dur+1)/2)
                mx=max(workers[a],workers[b])
                
                workers[a]=mx
                workers[b]=mx
                
                workers[a] += self._toFill(workers[a],half)
                workers[b] += self._toFill(workers[b],half)
                
                workers[a] +=half
                workers[b] +=half
                
        return max(workers)
    
    def order_crossover(self, other):
        c1 = TimeTable([])
        c2 = TimeTable([])
        mp1 = {}
        mp2 = {}
        
        start = randint(len(self.tasks))
        end = randint(start,len(self.tasks))
        
        for ind in range(start,end+1):
            mp1[self.tasks[ind][0]]=True
            mp2[other.tasks[ind][0]]=True
            
        for ind in range(len(self.tasks)):
            t1 = self.tasks[ind]
            t2 = other.tasks[ind]
            id1 = t1[0]
            id2 = t2[0]
            
            if id1 not in mp2:
                c1.tasks.append(t1)
            if id2 not in mp1:
                c2.tasks.append(t2)
                
        for ind in range(start,end+1):
            c1.tasks.append(other.tasks[ind])
            c2.tasks.append(self.tasks[ind])
            
        return (c1,c2)
    
    def uniform_crossover(self, other):
        c1 = TimeTable([(0,0,0)]*len(self.tasks))
        c2 = TimeTable([(0,0,0)]*len(self.tasks))
        c1.tasks = self.tasks.copy()
        c2.tasks = other.tasks.copy()
        
        for ind in range(len(self.tasks)):
            if rand()>0.5: 
                c1.tasks[ind] = (self.tasks[ind][0],self.tasks[ind][1],other.tasks[ind][2])
                c2.tasks[ind] = (other.tasks[ind][0],other.tasks[ind][1],self.tasks[ind][2])
            else:
                c1.tasks[ind] = (self.tasks[ind][0],self.tasks[ind][1],self.tasks[ind][2])
                c2.tasks[ind] = (other.tasks[ind][0],other.tasks[ind][1],other.tasks[ind][2])
        
        return (c1,c2)
    
    def mutate(self):
        start = randint(len(self.tasks)-1)
        end = randint(start+1,len(self.tasks))
        self.tasks.insert(start, self.tasks.pop(end))
            
    def _timesPerWorker(self):
        worker2times = [[] for _ in range(WORKERS_CNT)]
        scheduled = [0 for _ in range(WORKERS_CNT)]
        
        for x in self.tasks:
            (id,dur,opt)=x
            (a,b) = options[opt]
            
            if a == b:
                tofill = self._toFill(scheduled[a],dur)
                if tofill>0 or (scheduled[a]>0 and scheduled[a]%DAY_LENGTH==0):
                    worker2times[a].append((-1,tofill))
                    scheduled[a]+=tofill
                    worker2times[a].append((-2,1))
                
                worker2times[a].append((id,dur))
                scheduled[a]+=dur
            
            else:
                lenA = scheduled[a]
                lenB = scheduled[b]
                
                ind = a
                toadd = lenB-lenA
                if lenB<lenA:
                    ind=b
                    toadd = lenA-lenB
                    
                if toadd>0:
                    if scheduled[ind]%DAY_LENGTH==0 and scheduled[ind]>0:
                            worker2times[ind].append((-2,1))
                    for i in range(toadd):
                        worker2times[ind].append((-1,1))
                        scheduled[ind]+=1
                        
                        if scheduled[ind]%DAY_LENGTH==0 and i < toadd-1:
                            worker2times[ind].append((-2,1))
            
                half = int((dur+1)/2)
                tofill = self._toFill(scheduled[a],half)
                
                if tofill>0 or (scheduled[a]>0 and scheduled[a]%DAY_LENGTH==0):
                    worker2times[a].append((-1,tofill))
                    worker2times[b].append((-1,tofill))
                    scheduled[a]+=tofill
                    scheduled[b]+=tofill
                    
                    worker2times[a].append((-2,1))
                    worker2times[b].append((-2,1))
                
                worker2times[a].append((id,half))
                worker2times[b].append((id,half))
                scheduled[a]+=half
                scheduled[b]+=half
                
        return worker2times
                
    def printAscii(self):
        worker2times = self._timesPerWorker()
        for times in worker2times:
            scheduleString = ""
            for (id,dur) in times:
                char=""
                if id==-1:
                    char="_"
                if id==-2:
                    char="|"
                elif id>=0:
                    char = tablePrintChars[id%len(tablePrintChars)]
                scheduleString+=char*dur
            print(scheduleString)
    
    def printColor(self):
        worker2times = self._timesPerWorker()
        EXT=2
        for times in worker2times:
            scheduleString = ""
            for (id,dur) in times:
                char=""
                color = colors[id%len(colors)]
                if id==-1:
                    char=colored(" "*EXT,None,None)
                if id==-2:
                    char=colored(" ",None,None)+colored("|",None,None)+colored(" ",None,None)
                elif id>=0:
                    char=colored(" "*EXT, None, color)
                    
                scheduleString+=char*dur
            print(scheduleString)
        
