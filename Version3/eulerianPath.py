from collections import defaultdict 

class vertex:

	def __init__(self,vert,parents,verts):
		self.v=vert
		self.parent=parents[vert]
		self.dist=((verts[self.parent][0]-verts[self.v][0])**2+(verts[self.parent][1]-verts[self.v][1])**2)**0.5

	def __lt__(self,other):
		return other.dist>self.dist



class Graph: 
  
    def __init__(self,mapping): 
        self.graph = defaultdict(list)
        self.path=[]
        self.helper_path=[]
        self.mapping=mapping

    def addEdge(self,u,v): 
        self.graph[u].append(v) 
 
    def DFSUtil(self,v,visited): 
        visited[v]= True 
        self.path.append(self.mapping[v])
        self.helper_path.append(v)

        for j in self.graph[v]: 
            i=j.v
            if visited[i] == False: 
                self.DFSUtil(i, visited) 
                #self.path.append(self.mapping[v])
               	#self.helper_path.append(v)
   
    def DFS(self,v,V): 
        visited = [False]*V
        self.DFSUtil(v,visited) 

def getPath(vertices,parents,mapping):
	V=len(vertices)
	g=Graph(mapping)
	for i in range(1,V):
		g.addEdge(parents[i],vertex(i,parents,vertices))

	for u in g.graph:
		g.graph[u].sort()

	g.DFS(0,V)
	return g.path, g.helper_path

