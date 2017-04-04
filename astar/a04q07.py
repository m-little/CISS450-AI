from Queue import PriorityQueue
import copy
import math


def move(direction, m, target=' '):
	x = 0
	while(x != len(m)):
		if m[x].count(target) != 0:
			y = m[x].index(target)
			if direction == 'N' and x > 0:
				m[x-1][y], m[x][y] = m[x][y], m[x-1][y]
			if direction == 'S' and x < len(m)-1:
				m[x+1][y], m[x][y] = m[x][y], m[x+1][y]
			if direction == 'E' and y < len(m[x])-1:
				m[x][y+1], m[x][y] = m[x][y], m[x][y+1]
			if direction == 'W' and y > 0:
				m[x][y-1], m[x][y] = m[x][y], m[x][y-1]
		x+=1
	return m

def matrix(s, seperator=','):
	s = s.split(seperator)
	n = int(len(s)**.5)
	temp = []
	for index in range(0,len(s),n):
		temp.append(s[index:n+index]) 

	return temp

class closed():
	def __init__(self):
		self.d = {}
	def __len__(self):
		return len(self.d)
	def put(self,x,e, h):
		self.d["%s" % x] = (e, h)
	def has(self,x):
		return self.d.has_key("%s" % x)
	def get(self,x):
		return self.d["%s" % x]

def turn_to_string(x):
	s = ''
	for i in x:
		s += ','.join(str(y) for y in i)
		s += '\\n'
	return s

def heuristic(state1,state2):
	ret = 0

	for i in range(len(state1)):
		for j in range(len(state1[i])):
			for x in range(len(state2)):
				try:
					y = state2[x].index(state1[i][j])
					ret += abs(x - i) + abs(y - j)
					break
				except:
					pass

	return ret

def get_path(initial_state, solution, Closed):
	route = []
	while not(initial_state == solution[1][0]):
		route.append(solution[1][1])
		if solution[1][1] == 'N': temp = move('S', solution[1][0])
		elif solution[1][1] == 'S': temp = move('N', solution[1][0])
		elif solution[1][1] == 'E': temp = move('W', solution[1][0])
		elif solution[1][1] == 'W': temp = move('E', solution[1][0])
		blah = Closed.get(temp)
		solution = (blah[1],(temp, blah[0]))

	route.reverse()
	return route

def GRAPH_SEARCH(initial_state, goal_state):
	F = PriorityQueue()
	#add initial state to the deque
	F.put( (heuristic(initial_state, goal_state),(initial_state,'', 0)) )
	max_fringe_length = F.qsize()
	#closed is the states that have already been seen
	Closed = closed()
	Closed.put(initial_state,'', heuristic(initial_state, goal_state))

	graph_file = file('./graphsearch.dot', 'w')
	graph_file.write('digraph GraphSearch {\n')
	graph_file.write('node[shape=box,style=filled, fillcolor=white]\n')

	node_nums = {}
	node_count = 0

	while not(F.empty()):
		# remove highest priority state from priority queue
		temp = F.get()
		Closed.put(temp[1][0],temp[1][1],temp[0])


		#print temp
		if not node_nums.has_key('%s' % temp[1][0]):
			graph_file.write('n%d[label="%s",fillcolor=white]\n' % (node_count, turn_to_string(temp[1][0])))
			node_nums['%s' % temp[1][0]] = node_count
			node_count += 1
		else:
			graph_file.write('n%d[fillcolor=white]\n' % node_nums['%s' % temp[1][0]])

		if temp[1][0] == goal_state:
			graph_file.write('n%d[fillcolor=blue]\n' % node_nums['%s' % temp[1][0]])
			graph_file.write('}')
			graph_file.close()

			return temp, Closed, F.qsize(), max_fringe_length


		for e in ['N','S','E','W']:
			state_temp = move(e,copy.deepcopy(temp[1][0]))
			next_state = (heuristic(goal_state, state_temp) + temp[1][2] + 1,(state_temp,e, temp[1][2] + 1))
			if not(Closed.has(next_state[0])) and temp[1][0] != next_state[0]:
				graph_file.write('n%d[label="%s"]\n' % (node_count, turn_to_string(next_state[1][0])))
				graph_file.write('n%d->n'% node_nums['%s' % temp[1][0]])
				graph_file.write('%d\n' % node_count)
				node_nums['%s' % next_state[1][0]] = node_count
				node_count += 1

				F.put(next_state)
				
		if F.qsize() > max_fringe_length:
			max_fringe_length = F.qsize()

	return None,Closed, 0, max_fringe_length

def SOLVE(initial_state):
	initial_state = matrix(initial_state)
	#generate solution
	f = matrix(','.join(str(x) for x in range (0,len(initial_state[0])**2-1))+ ', ')
	solution,Closed,len_f, max_length_f = GRAPH_SEARCH(initial_state, f)
	
	#len_c = 0

	len_c = len(Closed)
	print solution[1][0], solution[1][1]
	route = []
	if solution != None:
		route = get_path(initial_state,solution,Closed)

		return route, max_length_f,len_c, len_f
	else: return None


	#print initial_state, f
	#GRAPH_SEARCH(initial_state,f,'bfs')


print SOLVE("0,1,2,3,4,5,6,7,8,9,10,11, ,12,13,14")
#print heuristic([[2,1,3],[4,5,7],[6,8,'']], [[1,2,3],[4,5,6],[7,8,'']])