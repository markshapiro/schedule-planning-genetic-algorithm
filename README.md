# schedule-planning-genetic-algorithm

### Problem Defintion

given n jobs, their durations (between 3 and 9 indivisible time units) and 5 workers.
```math
\begin{flalign}
& j_1, j_2, ... j_n &
\end{flalign}
```
```math
\begin{flalign}
& \forall duration(j_i) \in ℕ &
\end{flalign}
```
```math
\begin{flalign}
& 3 \leq duration(j_i) \leq 9 &
\end{flalign}
```

the goal is to create time schedule where all jobs would be assigned to workers while minimizing the timespan (time between start of 1st task and finish of last) using following rules:
1) each worker can only work on 1 job per time
2) each job can be assigned to 1 or 2 workers (out of any 5 workers)
3) order of job execution doesn't matter
4) if a job is assigned to 2 workers, they must start and finish together at the same time
5) if a job is assigned to 2 workers, the job duration will be split by 2, if duration is odd number then both workers will work until the end of last time unit (e.g. if job duration is 7, they wil both work 4 time units)
6) workers have a window of 18 time units per day, during which they can be assigned jobs, makespan of daily schedule of worker shouldn't exceed 18 time units.
7) workers can have idle time between jobs.
8) jobs can't be split to smaller jobs, only between 2 workers

### Solution

crossover and mutation in GA inspired by this paper: https://www.researchgate.net/publication/281545095_SOLVING_JOB_SHOP_SCHEDULING_PROBLEM_WITH_GENETIC_ALGORITHM

### Sample Run

example run for randomly generated jobs:

makespan reduction with each iteration:

![http://url/to/img.png](https://github.com/markshapiro/schedule-planning-genetic-algorithm/raw/main/iterations.jpg)

best solution for 5 workers accross 5 days:

![http://url/to/img.png](https://github.com/markshapiro/schedule-planning-genetic-algorithm/raw/main/timetable.jpg)
