import eulerianPath
import copy
MAX_INT=1000000
class Graph(): 

	def __init__(self, vertices,mapping): 
		self.vertices = vertices
		self.map=mapping
		self.V = len(vertices) 

	def printMST(self, parent): 
		print("Edge \tWeight")
		for i in range(1,self.V): 
			print(parent[i],"-",self.map[i],"\t",self.dist(u,v)) 

	def minKey(self, key, mstSet): 

		min_key = MAX_INT 

		for v in range(self.V): 
			if key[v] < min_key and mstSet[v] == False: 
				min_key = key[v] 
				min_index = v 

		return min_index 

	def dist(self,u,v):
		return ((self.vertices[u][0]-self.vertices[v][0])**2+(self.vertices[u][1]-self.vertices[v][1])**2)**0.5
	

	def primMST(self): 

		key = [MAX_INT] * self.V 
		parent = [None] * self.V
		helper_parent = [None] * self.V

		key[0] = 0
		mstSet = [False] * self.V 

		parent[0] = -1
		helper_parent[0] = -1

		for cout in range(self.V): 

			u = self.minKey(key, mstSet) 

			mstSet[u] = True

			for v in range(self.V): 
				if self.dist(u,v)>0 and mstSet[v] == False and key[v] > self.dist(u,v): 
					key[v] = self.dist(u,v)
					parent[v] = self.map[u] 
					helper_parent[v] = u

		#self.printMST(parent)
		return parent,helper_parent


def getPaths(vertices,mapping):
	g = Graph(vertices,mapping)

	parent,helper_parent=g.primMST()

	path, helper_path=eulerianPath.getPath(vertices,helper_parent,mapping)
	#print(path,len(path),len(helper_path))
	V=len(vertices)

	maxMstCost=0
	for i in range(1,V):
		maxMstCost+=g.dist(helper_parent[i],i)
	maxMstCost*=2
	#print(maxMstCost)
	T=maxMstCost/2
	start=0
	end=maxMstCost
	while abs(start-end)>0.2:
		T=(start+end)/2
		index=0
		for i in range(2):
			index+=1
			pathLength=0
			if i==1:
				pathLength=g.dist(helper_path[0],helper_path[index-1])
			while index<len(helper_path) and pathLength+g.dist(helper_path[index-1],helper_path[index])<=T:
				pathLength+=g.dist(helper_path[index-1],helper_path[index])
				index+=1
			#print(i,":",pathLength)
			if index>=len(helper_path):
				break

		if index<len(helper_path):
			start=T+1
		else:
			end=T
		#print(start,T,end)

	T=end
	P=[[],[]]
	pathLength=[0,0]
	index=0
	for i in range(2):
		X=[path[index]]
		index+=1
		if i==1:
			pathLength[1]=g.dist(helper_path[0],helper_path[index-1])
		while index<len(helper_path) and pathLength[i]+g.dist(helper_path[index-1],helper_path[index])<=T:
			X.append(path[index])
			pathLength[i]+=g.dist(helper_path[index-1],helper_path[index])
			index+=1

		P[i]=copy.deepcopy(X)
		if index>=len(helper_path):
			break

	X=[]
	for i in P[1]:
		X=[i]+X
	#P[1]=copy.deepcopy(X)
	#print(index,g.dist(helper_path[-2],helper_path[-1]))
	#print("T:",T,"\n1:",P[0],"\n2:",P[1])
	#print("T:",T,pathLength[0],pathLength[1])
	return parent, P, pathLength




"""
distances=[ [0, 2, 0, 6, 0], 
            [2, 0, 3, 8, 5], 
            [0, 3, 0, 0, 7], 
            [6, 8, 0, 0, 9], 
            [0, 5, 7, 9, 0]]
MST([0,1,2,4],distances)
"""


def getMST(vertices,mapping):
	g = Graph(vertices,mapping)

	parent,helper_parent=g.primMST()

	path, helper_path=eulerianPath.getPath(vertices,helper_parent,mapping)

	return parent,path