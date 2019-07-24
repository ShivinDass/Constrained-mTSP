
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


def MST(vertices,mapping):
	g = Graph(vertices,mapping)

	parent,helper_parent=g.primMST();

	V=len(vertices)
	depth=[-1]*V
	depth[0]=0
	count=1
	while count<V:
		count=1
		for i in range(1,V):
			if depth[helper_parent[i]]>=0:
				depth[i]=depth[helper_parent[i]]+1
				count+=1

	return parent,depth


"""
distances=[ [0, 2, 0, 6, 0], 
            [2, 0, 3, 8, 5], 
            [0, 3, 0, 0, 7], 
            [6, 8, 0, 0, 9], 
            [0, 5, 7, 9, 0]]
MST([0,1,2,4],distances)
"""