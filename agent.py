def readFile(fileName):
	gameMode = None
	color = None
	rTime = None
	board = []
	array1 = {'0+0':1,'0+1':1,'0+2':1,'0+3':1,'0+4':1,'1+0':1,'1+1':1,'1+2':1,'1+3':1,'1+4':1,'2+0':1,'2+1':1,'2+2':1,'2+3':1,'3+0':1,'3+1':1,'3+2':1,'4+0':1,'4+1':1}
	array2 = {'11+14':1,'11+15':1,'12+13':1,'12+14':1,'12+15':1,'13+12':1,'13+13':1,'13+14':1,'13+15':1,'14+11':1,'14+12':1,'14+13':1,'14+14':1,'14+15':1,'15+11':1,'15+12':1,'15+13':1,'15+14':1,'15+15':1}
	f = open(fileName, 'r')
	content = f.readlines()
	f.close()
	# SAVING GAME MODE, COLOR, RTIME
	gameMode = content[0].strip()
	color = content[1].strip()
	rTime = float(content[2].strip())
	# SAVING BOARD
	for i in range(3, 19):
		array = []
		for c in (content[i].strip()):
			array.append(c)
		board.append(array)
	# SAVING MY AND OPPONENTS CONFIG (INITIAL)
	if color=='BLACK':
		myconfig = {}
		x,y = 1,1
		oppconfig = {}
		camparray = array1
		goalarray = array2
		for i in range(0,len(board)):
			for j in range(0,len(board)):
				if board[i][j]=='B':
					myconfig[x]=['B',i,j]
					x+=1
				if board[i][j]=='W':
					oppconfig[y] = ['W',i,j]
					y+=1

	else:
		myconfig = {}
		x,y = 1,1
		oppconfig = {}
		camparray = array2
		goalarray = array1
		for i in range(0,len(board)):
			for j in range(0,len(board)):
				if board[i][j]=='W':
					myconfig[x]=['W',i,j]
					x+=1
				if board[i][j]=='B':
					oppconfig[y] = ['B',i,j]
					y+=1
	
	return gameMode, color, rTime, board, myconfig, oppconfig, camparray, goalarray



class gameTreeNode:
	def __init__(self,myplayer,myconfig,oppconfig,board, camparray, goalarray):
		self.myconfig = myconfig
		self.oppconfig = oppconfig
		self.myplayer = myplayer
		self.board = board
		self.camparray = camparray
		self.goalarray = goalarray

	def alphaBeta(self, depth,player, pawn, maximizingPlayer, goalarray, camparray, aplha, beta):
		if depth==0:
			return self.getutility(player),None
		else:
			if maximizingPlayer:
				value = float('-inf')
				mychildren = self.validMoves(pawn,self.myconfig,goalarray,camparray)
				bestmove = None
				for x,mychild in mychildren:
					self.board,self.myconfig = self.getnewconfig(mychild[1][0],mychild[1][-1],self.myconfig,pawn)
					for opponent in self.oppconfig.items():
						new_value, move = self.alphaBeta(depth-1,player,opponent,False,camparray,goalarray,aplha,beta)
						aplha = max(aplha,value)
						if value<new_value:
							value = new_value
							bestmove = mychild
						if value>=beta:
							break

						
					self.board,self.myconfig = self.getnewconfig(mychild[1][-1],mychild[1][0],self.myconfig,pawn)
				if value==float('-inf'):
					return float('inf'), None

				return value, bestmove
			else:
				value = float('inf')
				oppchildren = self.validMoves(pawn, self.oppconfig, goalarray, camparray)
				bestmove = None

				for x,oppchild in oppchildren:
					self.board,self.oppconfig = self.getnewconfig(oppchild[1][0],oppchild[1][-1],self.oppconfig,pawn)
					for mypawn in self.myconfig.items():
						new_value, move = self.alphaBeta(depth-1,player,mypawn,True,camparray, goalarray,aplha,beta)
						beta = min(beta,value)
						if value > new_value:
							value = new_value
							bestmove = oppchild
						if value<=aplha:
							# pruned+=1
							break
						
					self.board,self.oppconfig = self.getnewconfig(oppchild[1][-1],oppchild[1][0],self.oppconfig,pawn)
				if value==float('inf'):
					return float('-inf'), None
				return value, bestmove

	def getutility(self,player):
		if self.myplayer == 'W':
			goal_positions = []
			opp_goal_positions = []
			evalu =0
			for pos,v in self.goalarray.items():
				position = pos.split('+')
				if self.board[int(position[0])][int(position[1])]!='W':
					goal_positions.append([int(position[0]),int(position[1])])

			for pos,v in self.camparray.items():
				position = pos.split('+')
				if self.board[int(position[0])][int(position[1])]!='B':
					opp_goal_positions.append([int(position[0]),int(position[1])])
			
			for player,value  in self.myconfig.items():
				array =[]
				for position in goal_positions:
					array.append(((value[1]-position[0])**2+(value[2]-position[1])**2)**0.5)
				if len(array)!=0:
					evalu+=max(array)
				else:
					evalu+=(-50)
			for player,value  in self.oppconfig.items():
				array =[]
				for position in opp_goal_positions:
					array.append(((value[1]-position[0])**2+(value[2]-position[1])**2)**0.5)
				if len(array)!=0:
					evalu-=max(array)
				else:
					evalu-=(-50)
			return -1*evalu

		elif self.myplayer=='B':
			goal_positions = []
			opp_goal_positions = []
			evalu = 0
			for pos,v in self.goalarray.items():
				position = pos.split('+')
				if self.board[int(position[0])][int(position[1])]!='B':
					goal_positions.append([int(position[0]),int(position[1])])

			for pos,v in self.camparray.items():
				position = pos.split('+')
				if self.board[int(position[0])][int(position[1])]!='W':
					opp_goal_positions.append([int(position[0]),int(position[1])])

			for player,value  in self.myconfig.items():
				array =[]
				for position in goal_positions:
					array.append(((value[1]-position[0])**2+(value[2]-position[1])**2)**0.5)
				if len(array)!=0:
					evalu+=max(array)
				else:
					evalu+=(-50)
			for player,value  in self.oppconfig.items():
				array =[]
				for position in opp_goal_positions:
					array.append(((value[1]-position[0])**2+(value[2]-position[1])**2)**0.5)
				if len(array)!=0:
					evalu-=max(array)
				else:
					evalu-=(-50)
			return -1*evalu


	

	def getnewconfig(self,src,destination,config,pawns):
		pawn = self.board[src[0]][src[1]]
		self.board[src[0]][src[1]] = self.board[destination[0]][destination[1]]
		self.board[destination[0]][destination[1]] = pawn

		config[pawns[0]][1] = destination[0]
		config[pawns[0]][2] = destination[1]
		return self.board, config


	def validMoves(self,pos,config, goalarray, camparray):
		if config[1][0]=='W':
			player = 'W'
			origin = [15,15]
			goal = [0,0]
		elif config[1][0]=='B':
			player = 'B'
			origin = [0,0]
			goal = [15,15]
		curr_x = pos[1][1]
		curr_y = pos[1][2]
		valid_moves = []
		mymap = self.validJ(curr_x,curr_y,{str(curr_x)+'+'+str(curr_y):[]},{str(curr_x)+'+'+str(curr_y):1})
		jumps = self.getjumppaths(mymap,curr_x,curr_y)
		if str(curr_x)+'+'+str(curr_y) in goalarray:
			########################################################################################
							## E in Goal
			for i in range(-1,2):
				for j in range(-1,2):
					next_x = curr_x+i
					next_y = curr_y+j
					if next_x<len(self.board) and next_x>=0 and next_y<len(self.board[0]) and next_y>=0:
						if str(next_x) + '+' + str(next_y) in goalarray:
							move = self.vaildE(curr_x,curr_y,next_x,next_y)
							if move is not None:
								valid_moves.append(move) 

			########################################################################################
							## Jump in Goal with check on destination
			for jump in jumps:
				jump = jump.split(',')
				destination = (jump[-1])
				jumpmove = []
				if destination in goalarray:
					for j in jump:
						x = j.split('+')[0]
						y = j.split('+')[1]
						jumpmove.append([int(x),int(y)])     
					valid_moves.append(['J',jumpmove])

		elif str(curr_x)+'+'+str(curr_y) in camparray:
			flag=True
			incamp=False
			if flag:
				######################################################################################
								## E outside camp
				for i in range(-1,2):
					for j in range(-1,2):
						next_x = curr_x+i
						next_y = curr_y+j
						if next_x<len(self.board) and next_x>=0 and next_y<len(self.board[0]) and next_y>=0:
							if str(next_x)+'+'+str(next_y) not in camparray:
								move = self.vaildE(curr_x,curr_y,next_x,next_y)
								if move is not None:
									valid_moves.append(move)
									flag=False
									incamp=True
				
				########################################################################################
							## Jump outside Camp with check on destination
				for jump in jumps:
					jump = jump.split(',')
					destination = (jump[-1])
					jumpmove = []
					if destination not in camparray:
						for j in jump:
							x = j.split('+')[0]
							y = j.split('+')[1]
							jumpmove.append([int(x),int(y)])      
						valid_moves.append(['J',jumpmove])
						flag=False
						incamp=True

			if flag:
				########################################################################################
							## E inside Camp with check on farther away
				for i in range(-1,2):
					for j in range(-1,2):
						next_x = curr_x+i
						next_y = curr_y+j
						if next_x<len(self.board) and next_x>=0 and next_y<len(self.board[0]) and next_y>=0:
							if str(next_x)+'+'+str(next_y) in camparray:
								move = self.vaildE(curr_x,curr_y,next_x,next_y)
								if move is not None:
									if self.isfarther(origin,move[1][0][0],move[1][0][1],move[1][1][0],move[1][1][1]):
										valid_moves.append(move)
										flag=False
				########################################################################################
							## Jump inside Camp with check on destination and farther away
				for jump in jumps:
					jump = jump.split(',')
					destination = (jump[-1])
					jumpmove = []
					if destination in camparray and self.isfarther(origin,curr_x,curr_y,int(destination.split('+')[0]),int(destination.split('+')[1])):
						for j in jump:
							x = j.split('+')[0]
							y = j.split('+')[1]
							jumpmove.append([int(x),int(y)])      
						valid_moves.append(['J',jumpmove])			
						## Added farther check 
						## No check on destination as E
						## jump to be implemented with a destination check
		else:
			########################################################################################
							## E anywhere with check on destination
			for i in range(-1,2):
				for j in range(-1,2):
					next_x = curr_x+i
					next_y = curr_y+j
					if next_x<len(self.board) and next_x>=0 and next_y<len(self.board[0]) and next_y>=0:
						if str(next_x)+'+'+str(next_y) not in camparray:
							move = self.vaildE(curr_x,curr_y,next_x,next_y)
							if move is not None:
								valid_moves.append(move)
			########################################################################################
							## Jump anywhere with check on destination
			for jump in jumps:
					jump = jump.split(',')
					destination = (jump[-1])
					jumpmove = []
					if destination not in camparray:
						for j in jump:
							x = j.split('+')[0]
							y = j.split('+')[1]
							jumpmove.append([int(x),int(y)])      
						valid_moves.append(['J',jumpmove])
			## check to only choose moves that are takint the pawn outside the camp
		
		return self.priority_moves(valid_moves,goal)

	

	def priority_moves(self,valid_moves,goal):
		priority_moves = {}
		for moves in valid_moves:
			destination = moves[1][-1]
			priority_moves[self.geteucldeian(goal,destination)] = moves

		return sorted(priority_moves.items(),key = lambda x: x[0])




			## outside camp
	def geteucldeian(self,goal,destination):

		return ((destination[0] - goal[0])**2+(destination[1] - goal[1])**2)**0.5

	def getjumppaths(self,mymap,curr_x,curr_y):
		queue = [[str(curr_x)+'+'+str(curr_y),None]]
		paths = []
		temp = {str(curr_x)+'+'+str(curr_y):str(curr_x)+'+'+str(curr_y)}
		while queue!=[]:
			element = queue.pop()
			generate_key = element[0]
			parent_key = element[1]
			if parent_key!=None and parent_key in temp:
				paths.append(temp[parent_key]+','+generate_key)
				temp[generate_key] = temp[parent_key]+','+generate_key

			if generate_key in mymap:
				children = mymap[generate_key]
				for child in children:
					queue.append([child,generate_key])
		return(paths)



	def vaildE(self,src_x,src_y,next_x,next_y):
		if self.board[next_x][next_y]=='.':
			return ['E',[[src_x,src_y],[next_x,next_y]]]
		return None


	def validJ(self,curr_x,curr_y,mymap,visited):
		if curr_x<len(self.board) and curr_x>=0 and curr_y<len(self.board[0]) and curr_y>=0:
			for i in range(-1,2):
				for j in range(-1,2):
					nearby_x = curr_x+i
					nearby_y = curr_y+j
					if nearby_x<len(self.board) and nearby_x>=0 and nearby_y<len(self.board[0]) and nearby_y>=0:
						if self.board[nearby_x][nearby_y]!='.':
							next_x = nearby_x+i
							next_y = nearby_y+j
							if str(next_x)+'+'+str(next_y) not in visited:
								if next_x<len(self.board) and next_x>=0 and next_y<len(self.board[0]) and next_y>=0 and self.board[next_x][next_y]=='.':
									if str(curr_x)+'+'+str(curr_y) not in mymap:
										mymap[str(curr_x)+'+'+str(curr_y)] = [str(next_x)+'+'+str(next_y)]
									else:
										mymap[str(curr_x)+'+'+str(curr_y)].append(str(next_x)+'+'+str(next_y))
									visited[str(next_x)+'+'+str(next_y)]=1
									self.validJ(next_x,next_y,mymap,visited)

		return mymap

	def isfarther(self,origin,curr_x,curr_y,next_x,next_y):
		origin_x = origin[0]
		origin_y = origin[1]
		current_distance = abs(curr_x-origin_x)+abs(curr_y-origin_y)
		new_distance = abs(next_x-origin_x)+abs(next_y-origin_y)
		if new_distance>current_distance:
			return True
		return False

	def iscloser(self,origin,curr_x,curr_y,next_x,next_y):
		origin_x = origin[0]
		origin_y = origin[1]
		current_distance = abs(curr_x-origin_x)+abs(curr_y-origin_y)
		new_distance = abs(next_x-origin_x)+abs(next_y-origin_y)
		if new_distance<current_distance:
			return True
		return False


	

def main():
	gameMode, color, rTime, board, myconfig, oppconfig, camparray, goalarray = readFile("./input.txt")
	depth = 2
	troops_inside = True
	value = float('-inf')
	bestmove = None
	best_pawn = None
	if color[0]=="B":
		player_turn_black("B",myconfig,oppconfig,board,camparray,goalarray,depth)
	else:
		player_turn_white("W",myconfig,oppconfig,board,camparray,goalarray,depth)
		

def player_turn_black(color,myconfig,oppconfig,board,camparray,goalarray,depth):
	troops_inside = True
	value = float('-inf')
	out_value = float('-inf')
	in_value = float('-inf')
	bestmove = None
	best_pawn = None
	troops_inside = True
	value = float('-inf')
	bestmove = None
	best_pawn = None
	treenode = gameTreeNode(color[0],myconfig,oppconfig,board,camparray,goalarray)
	troops_inside = True
	out_move = False
	if troops_inside:
		for pawn in myconfig.items():
			if str(pawn[1][1])+'+'+str(pawn[1][2]) in camparray:
				newvalue, move = treenode.alphaBeta(depth-1,color[0],pawn,True,goalarray, camparray,float('-inf'),float('inf'))
				if newvalue==float('inf') or newvalue==float('-inf'):
					continue
				destination = move[1][-1]
				if str(destination[0])+'+'+str(destination[1]) not in camparray:
					if in_value<newvalue:
						troops_inside = False
						in_value = newvalue
						bestmove = move
						best_pawn = pawn
						out_move = True
				if not out_move:
					if out_value<newvalue:
						troops_inside = False
						out_value = newvalue
						bestmove = move
						best_pawn = pawn
	if troops_inside:
		for pawn in myconfig.items():
			newvalue, move = treenode.alphaBeta(depth-1,color,pawn,True,goalarray, camparray,float('-inf'),float('inf'))
			if newvalue==float('inf') or newvalue==float('-inf'):
				continue
			if value<newvalue:
				value = newvalue
				bestmove = move
				best_pawn = pawn

	f = open('output.txt','w+')
	type_of_move = bestmove[0]
	moves = bestmove[1]
	src = moves[0]
	for i in range(1,len(moves)):
		string = type_of_move +' '+ str(src[1])+','+str(src[0]) + ' ' + str(moves[i][1])+','+str(moves[i][0])+'\n'
		f.write(string)
		src = moves[i]
	f.close()

def player_turn_white(color,myconfig,oppconfig,board,camparray,goalarray,depth):
	value = float('-inf')
	out_value = float('-inf')
	in_value = float('-inf')
	bestmove = None
	best_pawn = None
	treenode = gameTreeNode(color[0],myconfig,oppconfig,board,camparray,goalarray)
	troops_inside = True
	out_move = False
	if troops_inside:
		for pawn in myconfig.items():
			if str(pawn[1][1])+'+'+str(pawn[1][2]) in camparray:
				newvalue, move = treenode.alphaBeta(depth-1,color[0],pawn,True,goalarray, camparray,float('-inf'),float('inf'))
				if newvalue==float('inf') or newvalue==float('-inf'):
					continue
				destination = move[1][-1]
				if str(destination[0])+'+'+str(destination[1]) not in camparray:
					if in_value<newvalue:
						troops_inside = False
						in_value = newvalue
						bestmove = move
						best_pawn = pawn
						out_move = True
				if not out_move:
					if out_value<newvalue:
						troops_inside = False
						out_value = newvalue
						bestmove = move
						best_pawn = pawn
	if troops_inside:
		for pawn in myconfig.items():
			newvalue, move = treenode.alphaBeta(depth-1,color,pawn,True,goalarray, camparray,float('-inf'),float('inf'))
			if newvalue==float('inf') or newvalue==float('-inf'):
				continue
			if value<newvalue:
				value = newvalue
				bestmove = move
				best_pawn = pawn

	f = open('output.txt','w+')
	type_of_move = bestmove[0]
	moves = bestmove[1]
	src = moves[0]
	for i in range(1,len(moves)):
		string = type_of_move +' '+ str(src[1])+','+str(src[0]) + ' ' + str(moves[i][1])+','+str(moves[i][0])+'\n'
		f.write(string)
		src = moves[i]
	f.close()
	
main()