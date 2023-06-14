# Trying out A start algorithm implementation
# pip install pyamaze
from pyamaze import maze, agent,COLOR,textLabel
from queue import PriorityQueue
# print(problem.maze_map)
# problem.run()

def heuristic_cost(cell_1, cell_2):
    x1, y1 = cell_1
    x2, y2 = cell_2
    return abs(x1-x2) + abs(y1-y2)

def a_star(problem):
    start = (problem.rows, problem.cols)
    # Create dicti for g score
    g_score = {cell:float('inf') for cell in problem.grid}
    g_score[start] = 0
    f_score = {cell:float('inf') for cell in problem.grid}
    f_score[start] = heuristic_cost(start, (1,1))

    # Create the priority queue
    que_q = PriorityQueue()
    que_q.put((f_score, heuristic_cost(start, (1,1)), start))

    path = {}
    searchPath = [start]
    while not que_q.empty():
        current_cell = que_q.get()[2]
        searchPath.append(current_cell)
        if current_cell == (1,1):
            break
        for d in 'EWNS':
            if problem.maze_map[current_cell][d] == True:
                if d == 'E':
                    new_cell = (current_cell[0], current_cell[1]+1)
                if d == 'W':
                    new_cell = (current_cell[0], current_cell[1]-1)
                if d == 'N':
                    new_cell = (current_cell[0]-1, current_cell[1])
                if d == 'S':
                    new_cell = (current_cell[0]+1, current_cell[1])

                temp_gscore = g_score[current_cell] + 1
                temp_fscore = temp_gscore + heuristic_cost(new_cell, (1,1))

                if temp_fscore < f_score[new_cell]:
                    g_score[new_cell] = temp_gscore
                    f_score[new_cell] = temp_fscore
                    que_q.put((temp_fscore, heuristic_cost(new_cell, (1,1)), new_cell))
                    path[new_cell] = current_cell

        # Reversing the path because it's saved in reverse way in the dictionary
    final_path={}
    cell=(1,1)
    while cell!=start:
        final_path[path[cell]]=cell
        cell=path[cell]
    return searchPath,path,final_path

if __name__ == '__main__':
    problem = maze(5, 5)
    problem.CreateMaze()
    searchPath,aPath,fwdPath=a_star(problem)
    a=agent(problem,footprints=True,color=COLOR.blue,filled=True)
    b=agent(problem,1,1,footprints=True,color=COLOR.yellow,filled=True,goal=(problem.rows,problem.cols))
    c=agent(problem,footprints=True,color=COLOR.red)

    problem.tracePath({a:searchPath},delay=300)
    problem.tracePath({b:aPath},delay=300)
    problem.tracePath({c:fwdPath},delay=300)

    l=textLabel(problem,'A Star Path Length',len(fwdPath)+1)
    l=textLabel(problem,'A Star Search Length',len(searchPath))
    problem.run()