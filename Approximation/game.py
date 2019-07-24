import pygame,random,copy,math
import paths

display_width=600
display_height=600

pygame.init()
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Game Window')
clock=pygame.time.Clock()


#######COLOR DEFINITION#########
Red=(255,0,0)
Blue=(0,0,255)
Green=(0,255,0)
Black=(0,0,0)
Yellow=(255,255,0)


################################
class Agent:
	def __init__(self,speed):
		self.radius=3
		self.commDist=COMM_DIST
		self.speed=speed
		self.x=tasks[0].x
		self.y=tasks[0].y
		self.path=[0]
		self.state=2
		self.currentTask=0
		self.currentPath=[]
		self.currentPartition=-1

	def update(self,x_pos,y_pos):
		self.x=x_pos
		self.y=y_pos

	def display(self):
		pygame.draw.circle(gameDisplay,Green,(self.x,self.y),self.radius)
		#pygame.draw.circle(gameDisplay,Yellow,(self.x,self.y),self.commDist,1)


	def nextTask(self):
		while len(self.currentPath)>0:
			if tasks[self.currentPath[0]].visited==False:
				t=self.currentPath.pop(0)
				self.currentTask=t
				return t
			else:
				self.currentPath.pop(0)
		return -1

	def dist(self, t):
		return ((self.x-t.x)**2+(self.y-t.y)**2)**0.5



class task:
	def __init__(self,x,y,identity):
		self.radius=4
		self.id=identity
		self.x=x
		self.y=y
		self.visited=False
		self.partition=-1

	def display(self):
		if self.visited:
			pygame.draw.circle(gameDisplay,Blue,(self.x,self.y),self.radius)
			return	
		pygame.draw.circle(gameDisplay,Red,(self.x,self.y),self.radius)

	def dist(self, t):
		return ((self.x-t.x)**2+(self.y-t.y)**2)**0.5


class partition:
	def __init__(self,centre):
		self.id=-1
		self.C=centre
		self.T=[]

	def addTask(self,i):
		if ((tasks[i].x-self.C[0])**2+(tasks[i].y-self.C[1])**2)**0.5<=COMM_DIST//2:
			self.T.append(i)
			tasks[i].partition=self.id
			#print(self.id)
			return True
		return False

	def display(self):
		pygame.draw.circle(gameDisplay,Black,(self.C[0],self.C[1]),COMM_DIST//2)
		pygame.draw.circle(gameDisplay,Yellow,(self.C[0],self.C[1]),COMM_DIST//2,1)



def initialize_tasks(numberTasks):
	t=[]
	t.append(task(5,5,0))
	t[0].visited=True
	i=1
	while i<numberTasks:
		X=task(random.randrange(5,display_width-5),random.randrange(5,display_height-5),i)
		flag=1
		for j in range(len(t)):
			if X.dist(t[j])<10:
				flag=0
				break
		if flag==1:
			t.append(copy.deepcopy(X))
			i+=1
	return t;

def generateGrid(N):
	t=[]

	d=display_width//N
	D=d
	xCoords=[0]
	for i in range(1,N-1):
		x=random.randrange(D-d//2,D+d//2)
		xCoords.append(x)
		D+=d
	xCoords.append(display_width-1)
	
	count=0
	for x in xCoords:
		for y in range(0,display_height,d): 
			t.append(task(x,y,count))
			count+=1
	t[0].visited=True
	return t

def drawMap():
	if mode==0:
		for i in range(len(partitions)-1,-1,-1):
			for j in range(len(partitions)):
				if partitions[j].id==i:
					partitions[j].display()
					break
	else:
		for i in range(len(partitions)-1,-1,-1):
			partitions[i].display()

	for i in range(numberTasks):
		tasks[i].display()


def visualizeMST(Parents,tasksRemaining):
	#print("Parents:",Parents)
	#print(tasksRemaining)
	for i in range(len(tasksRemaining)):
		pygame.draw.line(gameDisplay,Yellow,(tasks[tasksRemaining[i]].x,tasks[tasksRemaining[i]].y),(tasks[Parents[i+1]].x,tasks[Parents[i+1]].y))

def visualizePaths(p):
	for i in range(len(p)-1):
		pygame.draw.line(gameDisplay,Yellow,(tasks[p[i]].x,tasks[p[i]].y),(tasks[p[i+1]].x,tasks[p[i+1]].y))


def findBest(part):
	minD=1000000
	t=-1
	for i in partitions[part].T:
		if max(tasks[i].dist(A[0]),tasks[i].dist(A[1]))<minD:
			minD=max(tasks[i].dist(A[0]),tasks[i].dist(A[1]))
			t=i
			#print(t,minD)

	return t


def game_loop():
	quit=False

	Xinit=[0,0]
	Yinit=[0,0]
	Xspeed=[0,0]
	Yspeed=[0,0]
	time=[0,0]
	followTime=[0,0]
	turn=0

	iterations=0
	tasksCompleted=1

	while 1>0:#tasksCompleted<numberTasks:
		iterations+=1

		if A[0].state==2 and A[1].state==2:
			A[0].currentPartition+=1
			A[1].currentPartition+=1

			part=A[0].currentPartition
			if part>=len(partitions):
				break

			b=findBest(part)
			#print("b:",b)
			if b==-1:
				continue

			tasksRemaining=partitions[part].T
			tasksRemaining.remove(b)
			#print(len(tasksRemaining))
			coordinates=[]
			for j in tasksRemaining:
				coordinates.append([tasks[j].x,tasks[j].y])

			mstParents, Paths, pathLength=paths.getPaths([[tasks[b].x,tasks[b].y]]+coordinates,[b]+tasksRemaining)
			visualizeMST(mstParents,tasksRemaining)
			pygame.display.update()
			clock.tick(200)
			#l=input("Input to cont.:")

			#print("A: ",abs(tasks[b].dist(tasks[A[0].currentTask])+pathLength[0]-tasks[b].dist(tasks[A[1].currentTask])-pathLength[1]))
			#print(tasks[b].dist(tasks[A[0].currentTask]),tasks[b].dist(tasks[A[1].currentTask]))
			#print(pathLength[0],pathLength[1])
			if (tasks[b].dist(tasks[A[0].currentTask])>tasks[b].dist(tasks[A[1].currentTask]) and pathLength[0]>pathLength[1]) or (tasks[b].dist(tasks[A[0].currentTask])<tasks[b].dist(tasks[A[1].currentTask]) and pathLength[0]<pathLength[1]):
				#print("yes")
				tmp=copy.deepcopy(Paths[0])
				Paths[0]=copy.deepcopy(Paths[1])
				Paths[1]=copy.deepcopy(tmp)
				pathLength[0],pathLength[1]=pathLength[1],pathLength[0]

			#print("B: ",abs(tasks[b].dist(tasks[A[0].currentTask])+pathLength[0]-tasks[b].dist(tasks[A[1].currentTask])-pathLength[1]))
			#print()
			Paths[0]=[A[0].currentTask]+[b]+Paths[0]
			Paths[1]=[A[1].currentTask]+[b]+Paths[1]
			#l=input("Input to cont.:")
			for p in Paths:
				gameDisplay.fill(Black)
				visualizePaths(p)
				pygame.display.update()
				clock.tick(200)
				#l=input("Input to cont.:")

			for i in range(numberAgents):
				A[i].currentPath=copy.deepcopy(Paths[i])
				A[i].state=0


		for i in range(numberAgents):
			if A[i].state==0:
				Xinit[i]=A[i].x
				Yinit[i]=A[i].y
				time[i]=0				

				newTask=A[i].nextTask()
				#print(i,":",newTask)
				#print(tasksRemaining)
				if newTask==-1:
					A[i].state=2
					continue
				else:
					A[i].state=1
	
				Xspeed[i]=(tasks[A[i].currentTask].x-A[i].x)/tasks[A[i].currentTask].dist(A[i])
				Yspeed[i]=(tasks[A[i].currentTask].y-A[i].y)/tasks[A[i].currentTask].dist(A[i])
				#print(i,":",A[i].currentTask,tasks[A[i].currentTask].x,tasks[A[i].currentTask].y)
		

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				quit=True
				pygame.quit()
		if quit:
			break

		gameDisplay.fill(Black)
		#######################DISPLAY########################

		drawMap()
		for i in range(numberAgents):
			if tasks[A[i].currentTask].dist(A[i])<=A[i].speed and (not A[i].state==2):
				A[i].state=0
				tasks[A[i].currentTask].visited=True
				tasksCompleted+=1
				#print(tasksCompleted)

			if A[i].state==1:
				A[i].update(math.floor(Xinit[i]+time[i]*Xspeed[i]),math.floor(Yinit[i]+time[i]*Yspeed[i]))
				time[i]+=1

			A[i].display()

		#print(A[0].currentTask,",",A[1].currentTask)
		pygame.display.update()
		clock.tick(500)

	print(seed,"Iterations:",iterations)

seed=0
random.seed(seed)
mode=1
gridMode=0
numberTasks=120
numberAgents=2
COMM_DIST=200
tasks=[]
if gridMode==1:
	N=15
	tasks=generateGrid(N)
	numberTasks=N*N
else:
	tasks=initialize_tasks(numberTasks)

#tasksRemaining=[]
#for i in range(1,numberTasks):
#	if tasks[0].dist(tasks[i])<300:
#		tasksRemaining.append(i)
#		tasks[i].display()
#pygame.display.update()

tasksNotAllocated=[i for i in range(numberTasks)]
#tasksRemaining.remove(0)

counterForID=0
partitions=[]


if mode==0:
	while len(tasksNotAllocated)>0:
		maxDense=0
		maxI=-1
		maxX=[]
		for i in tasksNotAllocated:
			X=[]
			for j in tasksNotAllocated:
				if tasks[i].dist(tasks[j])<=COMM_DIST//2:
					X.append(j)

			if len(X)>maxDense:
				maxDense=len(X)
				maxI=i
				maxX=copy.deepcopy(X)


		partitions.append(partition([tasks[maxI].x,tasks[maxI].y]))
		partitions[-1].T=copy.deepcopy(maxX)
		partitions[-1].id=len(partitions)-1

		for k in maxX:
			tasksNotAllocated.remove(k)
			tasks[k].partition=len(partitions)-1

	mapping=[i for i in range(len(partitions))]
	mapping.remove(tasks[0].partition)

	coordinates=[]
	for j in mapping:
		coordinates.append([partitions[j].C[0],partitions[j].C[1]])

	b=tasks[0].partition
	mstParents,p=paths.getMST([[partitions[b].C[0],partitions[b].C[1]]]+coordinates,[b]+mapping)

	newPart=[]
	for i in p:
		newPart.append(partitions[i])

	partitions=copy.deepcopy(newPart)

else:
	for y in range(0,display_height+1,COMM_DIST//2):
		X=[]
		if y%COMM_DIST==0:
			for x in range(COMM_DIST//2,display_width+1,COMM_DIST):
				X=X+[partition([x,y])]
		else:
			for x in range(0,display_width+1,COMM_DIST):
				X=[partition([x,y])]+X

		for i in range(len(X)):
			X[i].id=counterForID
			counterForID+=1

		partitions=partitions+copy.deepcopy(X)

	for i in range(len(tasks)):
		j=0
		while not partitions[j].addTask(i):
			j+=1 


A=[]
A.append(Agent(1))
A.append(Agent(1))

game_loop()