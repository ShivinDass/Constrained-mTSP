import pygame,random,copy,math
import mst

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
		self.state=0
		self.currentTask=0

	def update(self,x_pos,y_pos):
		self.x=x_pos
		self.y=y_pos

	def display(self):
		pygame.draw.circle(gameDisplay,Green,(self.x,self.y),self.radius)
		pygame.draw.circle(gameDisplay,Yellow,(self.x,self.y),self.commDist,1)

	def addToPath(self,t):
		self.path.append(t)

	def getCurrentPos(self):
		return self.path[len(self.path)-1]

	def lengthTravelled(self):
		totalD=0
		for i in range(len(self.path)-1):
			totalD+=distance[self.path[i]][self.path[i+1]]
		return totalD

	def dist(self, t):
		return ((self.x-t.x)**2+(self.y-t.y)**2)**0.5


class task:
	def __init__(self,x,y,identity):
		self.radius=4
		self.id=identity
		self.x=x
		self.y=y
		self.visited=False

	def display(self):
		if self.visited:
			pygame.draw.circle(gameDisplay,Blue,(self.x,self.y),self.radius)
			return	
		pygame.draw.circle(gameDisplay,Red,(self.x,self.y),self.radius)

	def dist(self, t):
		return ((self.x-t.x)**2+(self.y-t.y)**2)**0.5

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
	for i in range(numberTasks):
		tasks[i].display()


def visualizeMST(Parents,j):
	#print(Parents)
	#print(tasksRemaining)
	for i in range(len(tasksRemaining)):
		if Parents[i+1]==-1:
			pygame.draw.line(gameDisplay,Yellow,(tasks[tasksRemaining[i]].x,tasks[tasksRemaining[i]].y),(A[j].x,A[j].y))
		#else:
		#	pygame.draw.line(gameDisplay,Yellow,(tasks[tasksRemaining[i]].x,tasks[tasksRemaining[i]].y),(tasks[Parents[i+1]].x,tasks[Parents[i+1]].y))


def findBestNode(depth,i):
	b=-1
	dep=numberTasks
	dist=100000
	for j in range(len(tasksRemaining)):				
		if depth[j+1]==1 and tasks[tasksRemaining[j]].dist(A[i])<dist:
			b=tasksRemaining[j]
			dep=depth[j+1]
			dist=tasks[tasksRemaining[j]].dist(A[i])
	return b




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

	while tasksCompleted<numberTasks:
		iterations+=1
		if A[0].state==0 and A[1].state==0 and mode:
			for i in range(numberAgents):
				coordinates=[]
				for j in tasksRemaining:
					coordinates.append([tasks[j].x,tasks[j].y])
				mstParents,depth=mst.MST([[A[i].x,A[i].y]]+coordinates,[-1]+tasksRemaining)
				b=findBestNode(depth,i)
				A[i].currentTask=b
			if tasks[A[0].currentTask].dist(A[0])<=tasks[A[1].currentTask].dist(A[1]):
				turn=0
			else:
				turn=1

		for k in range(numberAgents):
			i=(k+turn)%2
			if A[i].state==0:
				Xinit[i]=A[i].x
				Yinit[i]=A[i].y
				time[i]=0
				followTime[i]=0

				coordinates=[]
				for j in tasksRemaining:
					coordinates.append([tasks[j].x,tasks[j].y])
				mstParents,depth=mst.MST([[A[i].x,A[i].y]]+coordinates,[-1]+tasksRemaining)
				visualizeMST(mstParents,i)
				pygame.display.update()
				b=findBestNode(depth,i)
				#l=input("Input to cont.:")
				newTask=-1
				if b==-1:
					newTask=A[(i+1)%2].currentTask
				else:
					newTask=b
					tasksRemaining.remove(newTask)
				
				A[i].currentTask=newTask
				if A[(i+1)%2].state==0 or tasks[newTask].dist(tasks[A[(i+1)%2].currentTask])<=COMM_DIST:
					A[i].state=1
				else:
					A[i].state=2
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
			if tasks[A[i].currentTask].dist(A[i])<=A[i].speed:
				A[i].state=0
				tasks[A[i].currentTask].visited=True
				tasksCompleted+=1

		for i in range(numberAgents):
			if A[i].state==1:
				A[i].update(math.floor(Xinit[i]+time[i]*Xspeed[i]),math.floor(Yinit[i]+time[i]*Yspeed[i]))
				time[i]+=1

			elif A[i].state==2:
				if A[(i+1)%2].state==0:
					A[i].state=0
					tasksRemaining.append(A[i].currentTask)
					'''
					Xinit[i]=A[i].x
					Yinit[i]=A[i].y
					time[i]=0
					Xspeed[i]=(tasks[A[i].currentTask].x-A[i].x)/tasks[A[i].currentTask].dist(A[i])
					Yspeed[i]=(tasks[A[i].currentTask].y-A[i].y)/tasks[A[i].currentTask].dist(A[i])
					'''
				else:
					if A[i].dist(A[(i+1)%2])<COMM_DIST-10:
						A[i].update(math.floor(Xinit[i]+time[i]*Xspeed[i]+followTime[i]*Xspeed[(i+1)%2]),math.floor(Yinit[i]+time[i]*Yspeed[i]+followTime[i]*Yspeed[(i+1)%2]))
						time[i]+=1
					else:
						k=(i+1)%2
						vec=[A[k].x-A[i].x,A[k].y-A[i].y]
						#print(vec[0]*(Xspeed[i]-Xspeed[k])+vec[1]*(Yspeed[i]-Yspeed[k]))
						if vec[0]*(Xspeed[i]-Xspeed[k])+vec[1]*(Yspeed[i]-Yspeed[k])>15:
							A[i].update(math.floor(Xinit[i]+time[i]*Xspeed[i]+followTime[i]*Xspeed[(i+1)%2]),math.floor(Yinit[i]+time[i]*Yspeed[i]+followTime[i]*Yspeed[(i+1)%2]))
							time[i]+=1
						else:
							A[i].update(math.floor(Xinit[i]+time[i]*Xspeed[i]+followTime[i]*Xspeed[(i+1)%2]),math.floor(Yinit[i]+time[i]*Yspeed[i]+followTime[i]*Yspeed[(i+1)%2]))
							followTime[i]+=1

			A[i].display()

		turn=(turn+(1-mode))%2

		#print(A[0].state,",",A[1].state)
		pygame.display.update()
		clock.tick(200)

	print(seed,"Iterations:",iterations)

seed=0
random.seed(seed)
mode=1
gridMode=0
numberTasks=60
numberAgents=2
COMM_DIST=100
tasks=[]
if gridMode==1:
	N=15
	tasks=generateGrid(N)
	numberTasks=N*N
else:
	tasks=initialize_tasks(numberTasks)

tasksRemaining=[i for i in range(numberTasks)]
tasksRemaining.remove(0)


distance=[]
for i in range(numberTasks):
	X=[]
	for j in range(numberTasks):
		X.append(tasks[i].dist(tasks[j]))
	distance.append(X)

A=[]
A.append(Agent(1))
A.append(Agent(1))

game_loop()