import heapq, math, random, copy, time, numpy, os

class Node:
    def __init__(self, x_pos, y_pos, dist, priority):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.dist = dist
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.x_pos == other.x_pos and self.y_pos == other.y_pos

    def __str__(self):              # returns a string usefull for debug'n and hash function
        return "(%d %d)" % (self.x_pos,self.y_pos)

class PriorityQueue:
    def __init__(self):
        self.pq = []

    def __len__(self):
        return len(self.pq)

    def __contains__(self,key):     # for 'in' operator
        return key in self.pq

    def push(self, node):
        heapq.heappush(self.pq, node)

    def pop(self):
        return heapq.heappop(self.pq)

    def replace(self, node):
        self.pq.remove(node)
        heapq.heappush(self.pq, node)

def initRoom():
    room = []
    wx1 = random.randrange(0,6)
    wy1 = random.randrange(2,9)
    wx2 = random.randrange(0,6)
    wy2 = random.randrange(2,9)
    while wy2 == wy1:
        wy2 = random.randrange(2,9)
    wx3 = random.randrange(0,6)
    wy3 = random.randrange(2,9)
    while wy3 in [wy1,wy2]:
        wy3 = random.randrange(2,9)

    for x in range(12):
        row = []
        for y in range(12):
            if x == 0 or x == 11 or y == 0 or y == 11:
                row.append('X')
            elif y == wy1 and x > wx1 and x <= wx1 + 5:
                row.append('X')
            elif y == wy2 and x > wx2 and x <= wx2 + 5:
                row.append('X')
            elif y == wy3 and x > wx3 and x <= wx3 + 5:
                row.append('X')
            else:
                row.append(' ')
        room.append(row)
    iy = random.randrange(1,11)
    oy = random.randrange(1,11)
    room[iy][1] = 'I'
    room[oy][10] = 'O'

    return (room, 1, iy, 10, oy)

def draw(room):
    for row in room:
        s_row = str(row)
        s_row = s_row.replace("'", '')
        s_row = s_row.replace(",", ' ')
        print s_row
    print '\n'

def move(room, state,d):
    x,y = state.x_pos, state.y_pos
    ret = copy.deepcopy(state)

    if d == 'N':    y -= 1
    elif d == 'S':  y += 1
    elif d == 'E':  x += 1
    elif d == 'W':  x -= 1
    elif d == 'NE':
        y -= 1
        x += 1
    elif d == 'SE':
        y += 1
        x += 1
    elif d == 'NW':
        y -= 1
        x -= 1
    elif d == 'SW':
        y += 1
        x -= 1

    if room[y][x] == 'X':   return None
    else:
        ret.x_pos = x
        ret.y_pos = y

        return ret

def h(state, other):
    return math.sqrt((state.x_pos - other.x_pos)*(state.x_pos - other.x_pos) + (state.y_pos - other.y_pos)*(state.y_pos - other.y_pos))

def reconstruct_path(room, came_from, current_node, start):
    room[current_node.y_pos][current_node.x_pos] = 'I'
    while current_node != start:
        current_node = came_from[str(current_node)]
        room[current_node.y_pos][current_node.x_pos] = 'P'
        #draw(room)

    return room


def Astar(room,start,goal):
    openset = PriorityQueue()    # The set of tentative nodes to be evaluated, initially containing the start node
    came_from = {}    # The map of navigated nodes.

    start.priority = h(start, goal)
    openset.push(start)

    while len(openset) > 0:
        current = openset.pop()

        if current.x_pos == goal.x_pos and current.y_pos == goal.y_pos:            
            return reconstruct_path(room,came_from, goal, start)
        
        os.system('clear')
        draw(reconstruct_path(copy.deepcopy(room),came_from, current, start))
        time.sleep(.1)

        for e in ['E','NE','NW','SE','SW','W', 'N','S']:
            neighbor = move(room, current, e)

            if neighbor != None:

                tentative_g_score = current.dist + h(current,neighbor)

                temp = None
                if came_from.has_key(str(neighbor)):
                    temp_node = came_from[str(neighbor)]
                    temp = temp_node.dist + h(current,neighbor)
                    if tentative_g_score >= temp:
                        continue

                if not(neighbor in openset) or temp != None:#tentative_g_score < temp:
                    came_from[str(neighbor)] = current
                    neighbor.dist = tentative_g_score
                    neighbor.priority = neighbor.dist + h(neighbor, goal)
                    if not(neighbor in openset):
                        openset.push(neighbor)
                    else:
                        openset.replace(neighbor)

    return None

room, ix, iy, ox, oy = initRoom()
start = Node(ix,iy,0,0)
goal = Node(ox,oy,0,0)

draw(room)
room = Astar(room, start, goal)
if room != None:
    os.system('clear')
    draw(room)

#room = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
#        ['X', 'I', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'O', 'X'],
#        ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', 'X'],
#        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', 'X'],
#        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
#ix, iy = 1,1
#ox,oy = 10, 8
#
#start = Node(ix,iy,0,0)
#goal = Node(ox,oy,0,0)
#
#draw(room)
#room = Astar(room, start, goal)
#if room != None:
#    draw(room)