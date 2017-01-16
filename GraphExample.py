"""
Graph methods for trial purposes.

G{classtree GraphObject}
"""



class GraphObject(object):
    """
    An object class. This has no local methods, only class methods.
    
    The intent is to provide a collection of factory methods for graph classes. 
    """
    def __init__(self):
        """
        No further initialization is necessary as this class never does anything.
        """
        pass
    
    @classmethod
    def fromFile(cls, fileName):
        """
        Reads in a graph from a file as a list of vertex pairs.
        
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type fileName: String
        @param fileName: The name of the file that contains the input data for a graph.
        @rtype: An object of type cls.
        @return: A graph corresponding to vertex-edge data from the given file. 
        """
        edges = []
        verts=set([])
        try:
            ff = open(fileName, 'r')
            for ll in ff:
                ss = ll.strip()
                ls = ss.split(" ")
                if len(ls)==2:
                    a, b = int(ls[0]), int(ls[1])
                    edges.append((a,b))
                    verts.update([a,b])
            
            ff.close()
            return cls(list(verts), edges)
        except IOError:
            return cls([], [])
            
    @classmethod
    def random(cls, vertCount, edgeCount):
        """
        Creates a graph with vertCount vertices and at most edgeCount edges in a random fashion.        
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type vertCount: int
        @param vertCount: The number of vertices this graph is to have.
        @type edgeCount: int
        @param edgeCount: The maximum number of edges this graph is to have. This is not exact as we do nothing to prevent duplicate edges. 
        @rtype: An object of type cls.
        @return: A random graph.  
        """
        import random 
        verts = range(vertCount)
        edges = [random.sample(verts, 2) for i in range(edgeCount)]
        return cls(verts, edges)
        
    @classmethod
    def complete(cls, size=3):
        """
        Creates a complete graph with vertCount vertices. Thus every pair of vertices is an edge.         
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type size: int
        @param size: The number of vertices this graph is to have.
        @rtype: An object of type cls.
        @return: A complete graph of size I{size}.  
        """
        verts = range(size)
        edges = [(i, j) for i in verts for j in range(i+1, size)]
        return cls(verts, edges)
        
    @classmethod
    def path(cls, length=3):
        """
        Creates a path graph with I{length} + 1 vertices. The length of a path is the number of edges so this path has length I{length}.       
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type length: int
        @param length: The number of vertices this graph is to have. This has to be one more than the length. 
        @rtype: An object of type cls.
        @return: A path graph of length I{length}.  
        """
        verts = range(length+1)
        edges = [(i, i+1) for i in range(length)]
        return cls(verts, edges)
        
    @classmethod
    def cycle(cls, length=3):
        """
        Creates a cycle graph with vertCount vertices. The length of a cycle is the number of edges which equals the number of vertices.       
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type length: int
        @param length: The number of vertices this graph is to have.  
        @rtype: An object of type cls.
        @return: A cycle graph of length I{length}.  
        """
        verts = range(length)
        edges = [(i, i+1) for i in range(length - 1)] + [(0, length - 1)]
        return cls(verts, edges)
        
    @classmethod
    def joinAtVert(cls, g1, g2, v1, v2):
        """
        Makes a new graph that collapses I{v1} in I{g1} to I{v2} in I{g2}. 
        Vertices in I{g2} are renamed with numbers higher than those in I{g1}.
        No other vertices are collapsed. 
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type g1: A graph object of type cls.
        @param g1: A graph.  
        @type g2: A graph object of type cls.
        @param g2: A graph. 
        @type v1: int
        @param v1: A vertex in I{g1}. 
        @type v2: int
        @param v2: A vertex in I{g2}. 
        @rtype: An object of type cls.
        @return: The graph obtained by making vertex I{v1} in graph I{g1} equal to vertex I{v2} in graph I{g2}.  
        """
        verts = g1.vertices
        tmpVerts = g2.vertices
        tmpVerts.remove(v2)
        offset = max(verts) + 1
        vertDict = dict([(v2, v1)] + [(u, u+offset) for u in tmpVerts])
        edges = g1.edges + [(vertDict[u], vertDict[v]) for u, v in g2.edges]
        return cls(verts + [vertDict[u] for u in tmpVerts], edges)
        
    @classmethod
    def collapseEdge(cls, g1, a, b):
        """
        Makes the graph minor of I{g1} that results from collapsing edge  I{(a,b)} in I{g1}. 
        The new vertex is named I{a}. 
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type g1: A graph object of type cls.
        @param g1: A graph.  
        @type a: int
        @param a: A vertex in I{g1}. 
        @type b: int
        @param b: A vertex in I{g1} such that I{(a,b)} is an edge of I{g1}. 
        @rtype: An object of type cls.
        @return: The graph minor obtained by collapsing edge I{(a,b)} in graph I{g1}.  
        """
        if g1.hasEdge(a, b):
            verts = g1.vertices
            verts.remove(b)
            useEdges = g1.edges
            edges = [(u, v) for u, v in useEdges if u!=b and v!=b]
            edges += [(u, a) for u, v in useEdges if u!=a and v==b]
            edges += [(a,v) for u, v in useEdges if u==b and a!=v]
            return cls(verts, edges)
        else:
            return g1
        
        
    @classmethod
    def copy(cls, g1):      
        """
        Makes the copy I{g1}. This can be used to convert from one type to another. 
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type g1: A graph object of type cls.
        @param g1: A graph.
        @rtype: An object of type cls.
        @return: A copy of graph I{g1}.  
        """
        return cls(g1.vertices, g1.edges)
        
    @classmethod
    def cleancopy(cls, g1):
        """
        Makes the copy I{g1} without any duplicated edges. This can be used to convert from one type to another. 
        
        @type cls: A subclass of B{GraphObject}. 
        @param cls: The class of object we wish to create.
        @type g1: A graph object of type cls.
        @param g1: A graph.
        @rtype: An object of type cls.
        @return: A copy of graph I{g1} with no duplicate edges.  
        """
        verts = g1.vertices
        edges = list(set(g1.edges))     ## eliminate duplicate edges
        return cls(verts, edges)
                


class Graph1(GraphObject):
    """
    A graph object implemented as a list of vertices and a list of edges.
    
    @ivar vertices: the vertices of the graph
    @ivar edges: the edges of the graph
    """
    def __init__(self, vertices, edges):
        """
        Graph initialization.      
        
        @type vertices: A list of int. 
        @param vertices: The vertices of the graph.
        @type edges: A list of pairs of int.
        @param edges: The edges of the graph. These may be reordered so that all pairs are of the form (min, max).
        @rtype: An object of type Graph1.
        @return: A graph.  
        """
        self.vertices = vertices                                ## a list of ints
        self.edges = [(min(x), max(x)) for x in edges]          ## a list of int-pairs, least first
            
        
    def __len__(self):
        """
        The size of the graph as given by the number of vertices.      
        
        @rtype: int
        @return: The number of vertices of the graph.  
        """
        return len(self.vertices)
        
    def __repr__(self):
        """
        A simple string representation of the graph as vertices followed by edges.
        """
        return "Vertices: " + str(self.vertices) + "\nEdges: " + str(self.edges)
        
    def __str__(self):
        """
        A simple string representation of the graph as vertices followed by edges.
        """
        return "Vertices: " + str(self.vertices) + "\nEdges: " + str(self.edges)
        
    def copy(self):
        """
        A copy of the graph. This is different from the classmethod in that it 
        copies into the same type. This is B{not} a deep copy. 
        """
        return Graph1(self.vertices, self.edges)
        
        
    def hasVertex(self, a):
        """
        Determines if a vertex is present in the graph. 
        
        @type a:int
        @param a: the name of a possible vertex.
        @rtype: Boolean
        @return: True iff the given vertex is a  vertex of this graph. 
        """
        return a in self.vertices
        
    def hasEdge(self, a, b):
        """
        Determines if an edge is present in the graph. 
        
        @type a:int
        @param a: the name of a possible vertex.
        @type b:int
        @param b: the name of a possible vertex.
        @rtype: Boolean
        @return: True iff the given edge I{(a,b)} is an edge of this graph. 
        """
        aa = min(a,b)
        bb = max(a,b)
        return (aa, bb) in self.edges
        
    def addVertex(self, a):
        """
        Adds a vertex to the graph. This is added without checking if is already present.
        
        @type a:int
        @param a: the name of a possible vertex.
        @rtype: None
        @return: Nothing, no return value is necessary. 
        """
        self.vertices.append(a)
        
    def addVertexCleanly(self, a):
        """
        Adds a vertex to the graph. This checks if it is already present and only adds it if it is not present.
        
        @type a:int
        @param a: the name of a possible vertex.
        @rtype: Boolean
        @return: True iff the vertex was actually added to the graph. 
        """
        if a not in self.vertices:
            self.vertices.append(a)
            return True
        return False
 
        
    def deleteVertex(self, a):
        """
        Deletes a vertex to the graph. 
        
        @type a:int
        @param a: the name of a possible vertex to remove.
        @rtype: None
        @return: Nothing, no return value is necessary. 
        """
        try:        ## If a is not present a ValueError is raised
            self.vertices.remove(a)
            self.edges = [ee for ee in self.edges if a not in ee]
        except ValueError:      ## this requires no response
            pass
        
    def addEdge(self, a, b):
        """
        Adds an edge to the graph. This checks if it is already present and only adds it if it is not present.
        Checking is done to determine if we need to add the endpoints as well. 
        
        @type a:int
        @param a: the name of a possible vertex.
        @type b:int
        @param b: the name of a possible vertex such that I{(a,b)} is the new edge.
        @rtype: Boolean
        @return: True iff the edge was actually added to the graph. 
        """
        if not self.hasEdge(a,b):
            if a in self.vertices and b in self.vertices:
                self.edges.append((min(a,b), max(a,b)))
            elif a in self.vertices:
                self.addVertex(b)
                self.edges.append((min(a,b), max(a,b)))
            elif b in self.vertices:
                self.addVertex(a)
                self.edges.append((min(a,b), max(a,b)))
            else:
                self.addVertex(a)
                self.addVertex(b)
                self.edges.append((min(a,b), max(a,b)))
            return True
        return False
            
    def addEdges(self, *newEdges):
        """
        Adds many edges to the graph.  
        
        @type newEdges: unpacked list of pairs of ints (internally it is a list but we don't see that).
        @param newEdges: pairs comprising new edges.
        @rtype: None
        @return: None
        """
        for ee in newEdges:
            self.addEdge(*ee)   ## the * is needed to unpack the pair ee
            
    def deleteEdge(self, a, b):
        """
        Deletes an edge of the graph. 
        
        @type a:int
        @param a: the name of one endpoint of the edge to remove.
        @type b:int
        @param b: the name of the other endpoint of the edge to remove.
        @rtype: None
        @return: Nothing, no return value is necessary. 
        """
        aa = min(a,b)
        bb = max(a,b)
        try:
            self.edges.remove((aa, bb))
        except ValueError:  ## no action taken here as the edge doesn't exist
            pass
        
    def degree(self, v):
        """
        Computes the degree of a vertex, ie the number of edges coming out of the vertex.
        
        @type v: int
        @param v: a vertex whose degree is to be computed.
        @rtype: int
        @return: the degree of I{v}.
        """
        return len([xx for xx in self.edges if v in xx])
        
    def degreeFn(self):
        """
        Computes the degree of all vertices.
        
        @rtype: dict of int:int pairs
        @return: a dict taking a vertex to the degree of that vertex. 
        """
        return dict([(v, self.degree(v)) for v in self.vertices])
        
    def isConnected1(self):
        """
        Determines if the graph is connected, ie there is at least one path between any two vertices. 
        The method used is bucketing using direct computation to merge buckets.
        All vertices in a single component end up in a single bucket. 
        
        Finally the graph is connected iff there is only one bucket. 
        
        @rtype: Boolean
        @return: True iff the graph is connected. 
        """
        buckets = dict([(v,v) for v in self.vertices])
        change = 1
        while change:
            change = 0
            for ee in self.edges:
                if buckets[ee[0]]!=buckets[ee[1]]:
                    change = 1
                    tmp = buckets[ee[1]]
                    for vv in buckets:
                        if buckets[vv] == tmp:
                            buckets[vv] = buckets[ee[0]]
                            
        return len(set(buckets.values())) == 1
        
    def isConnected2(self):
        """
        Determines if the graph is connected, ie there is at least one path between any two vertices. 
        The method used is bucketing using a find-union process to merge buckets. 
        
        Finally the graph is connected iff there is only one bucket. 
        
        @rtype: Boolean
        @return: True iff the graph is connected. 
        """
        buckets=dict([(v, v) for v in self.vertices])
        def find(v):
            ff = buckets[v]
            if ff == v:
                ## print "one :", v
                return v
            else:
                f2 = find(ff)
                buckets[v] = f2
                ## print "two:", v, f2
                return f2
                
        change = 1
        valuesCnt = len(self.vertices)
        while change:
            change = 0
            for ee in self.edges:
                ff = find(ee[0])
                gg = find(ee[1])
                if ff!=gg:
                    change = 1
                    valuesCnt -= 1
                    buckets[gg] = ff
                    
        return valuesCnt == 1
                    
        
                            
        
        
class Graph2(GraphObject):
    """
    A graph object implemented as an adjacency dict.
    
    @ivar graph: a dictionary of vertex:list of adjacent vertices pairs. 
    """
    def __init__(self, vertices, edges):
        """
        Graph initialization.      
        
        @type vertices: A list of int. 
        @param vertices: The vertices of the graph.
        @type edges: A list of pairs of int.
        @param edges: The edges of the graph. These may be reordered so that all pairs are of the form (min, max).
        @rtype: An object of type Graph2.
        @return: A graph.  
        """
        self.graph = dict([(v, []) for v in vertices])          ## a dict int:list of int
        for ee in edges:
            self.graph[ee[0]].append(ee[1])
            self.graph[ee[1]].append(ee[0])
        
    @property
    def vertices(self):
        """
        A list of all vertices.
        """
        return self.graph.keys()
        
    @property
    def edges(self):
        """
        A list of all edges.
        """
        edges = [(u, v) for u in self.graph.keys() for v in self.graph[u] if u < v]
        return edges
    
    def __len__(self):
        """
        The size of the graph as given by the number of vertices.      
        
        @rtype: int
        @return: The number of vertices of the graph.  
        """
        return len(self.graph)
        
    def __repr__(self):
        """
        A simple string representation of the graph as vertices followed by edges.
        """
        edges = []
        for vv in self.graph:
            edges += [(uu, vv) for uu in self.graph[vv] if uu<vv]
        return "Vertices: " + str(self.graph.keys()) + "\nEdges: " + str(edges)
        
    def __str__(self):
        """
        A simple string representation of the graph as vertices followed by edges.
        """
        edges = []
        for vv in self.graph:
            edges += [(uu, vv) for uu in self.graph[vv] if uu<vv]
        return "Vertices: " + str(self.graph.keys()) + "\nEdges: " + str(edges)
        
    def copy(self):
        """
        A copy of the graph. This is different from the classmethod in that it 
        copies into the same type. This is B{not} a deep copy. 
        """
        return Graph2(self.vertices, self.edges)
        
    def hasVertex(self, a):
        """
        Determines if a vertex is present in the graph. 
        
        @type a:int
        @param a: the name of a possible vertex.
        @rtype: Boolean
        @return: True iff the given vertex is a  vertex of this graph. 
        """
        return a in self.graph
        
    def hasEdge(self, a, b):
        """
        Determines if an edge is present in the graph. 
        
        @type a:int
        @param a: the name of a possible vertex.
        @type b:int
        @param b: the name of a possible vertex.
        @rtype: Boolean
        @return: True iff the given edge I{(a,b)} is an edge of this graph. 
        """
        return a in self.graph and b in self.graph[a]
        
    def addVertex(self, a):
        """
        Adds a vertex to the graph. This is added without checking if is already present
        and so may have the side-effect of deleting all adjacency information attached to I{a}.
        
        @type a:int
        @param a: the name of a possible vertex.
        @rtype: None
        @return: Nothing, no return value is necessary. 
        """
        self.graph[a] = []
        
    def addVertexCleanly(self, a):
        """
        Adds a vertex to the graph. This checks if it is already present and only adds it if it is not present.
        
        @type a:int
        @param a: the name of a possible vertex.
        @rtype: Boolean
        @return: True iff the vertex was actually added to the graph. 
        """
        if a not in self.graph:
            self.graph[a] = []
            return True
        return False
        
    def deleteVertex(self, a):
        """
        Deletes a vertex to the graph. 
        
        @type a:int
        @param a: the name of a possible vertex to remove.
        @rtype: None
        @return: Nothing, no return value is necessary. 
        """
        try:
            otherVerts = self.graph[a][:]
            del self.graph[a]
            for xx in otherVerts:
                self.graph[xx].remove(a)
        except KeyError:
            pass
        
    def addEdge(self, a, b):
        """
        Adds an edge to the graph. This checks if it is already present and only adds it if it is not present.
        Checking is done to determine if we need to add the endpoints as well. 
        
        @type a:int
        @param a: the name of a possible vertex.
        @type b:int
        @param b: the name of a possible vertex such that I{(a,b)} is the new edge.
        @rtype: Boolean
        @return: True iff the edge was actually added to the graph. 
        """
        if not self.hasEdge(a,b):
            if a in self.graph and b in self.graph:
                self.graph[a].append(b)
                self.graph[b].append(a)
            elif a in self.graph:
                self.graph[a].append(b)
                self.graph[b] = [a]
            elif b in self.graph:
                self.graph[a] = [b]
                self.graph[b].append(a)
            else:
                self.graph[a] = [b]
                self.graph[b] = [a]
            return True       
        return False
            
    def addEdges(self, *newEdges):
        """
        Adds many edges to the graph.  
        
        @type newEdges: unpacked list of pairs of ints (internally it is a list but we don't see that).
        @param newEdges: pairs comprising new edges.
        @rtype: None
        @return: None
        """
        for ee in newEdges:
            self.addEdge(*ee)
            
    def deleteEdge(self, a, b):
        """
        Deletes an edge of the graph. 
        
        @type a:int
        @param a: the name of one endpoint of the edge to remove.
        @type b:int
        @param b: the name of the other endpoint of the edge to remove.
        @rtype: None
        @return: Nothing, no return value is necessary. 
        """
        try:
            self.graph[a].remove(b)
            self.graph[b].remove(a)
        except ValueError:
            pass
        
    def degree(self, v):
        """
        Computes the degree of a vertex, ie the number of edges coming out of the vertex.
        
        @type v: int
        @param v: a vertex whose degree is to be computed.
        @rtype: int
        @return: the degree of I{v}.
        """
        return len(self.graph[v])
        
    def degreeFn(self):
        """
        Computes the degree of all vertices.
        
        @rtype: dict of int:int pairs
        @return: a dict taking a vertex to the degree of that vertex. 
        """
        return dict([(v, self.degree(v)) for v in self.graph])
        
    def isConnected1(self):
        """
        Determines if the graph is connected, ie there is at least one path between any two vertices. 
        The method used is bucketing using direct computation to merge buckets.
        All vertices in a single component end up in a single bucket. 
        
        Finally the graph is connected iff there is only one bucket. 
        
        @rtype: Boolean
        @return: True iff the graph is connected. 
        """
        buckets = dict([(v,v) for v in self.graph])
        change = 1
        while change:
            change = 0
            for u in self.graph:
                newComp = [buckets[v] for v in self.graph[u] if buckets[u]!=buckets[v]]
                if len(newComp):
                     change = 1
                     for vv in buckets:
                        if buckets[vv] in newComp:
                            buckets[vv] = buckets[u]
                            
        return len(set(buckets.values())) == 1

    def isConnected2(self):
        """
        Determines if the graph is connected, ie there is at least one path between any two vertices. 
        The method used is bucketing using a find-union process to merge buckets. 
        
        Finally the graph is connected iff there is only one bucket. 
        
        @rtype: Boolean
        @return: True iff the graph is connected. 
        """
        buckets=dict([(v, v) for v in self.graph])
        valuesCnt = len(self.graph)
        def find(v):
            ff = buckets[v]
            if ff == v:
                ## print "one :", v
                return v
            else:
                f2 = find(ff)
                buckets[v] = f2
                ## print "two:", v, f2
                return f2
                
        change = 1
        while change:
            change = 0
            for u in self.graph:
                for v in self.graph[u]:
                    ff = find(u)
                    gg = find(v)
                    if ff!=gg:
                        change = 1
                        valuesCnt -= 1
                        buckets[gg] = ff
                    
        
        return valuesCnt == 1
        


def test(enum=0):
    if enum==1:
        tester = Graph1([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])
        print tester
        
        tester.addEdge(5,2)
        print tester
        
        tester.deleteVertex(1)
        print(tester)
        
        tester.addEdges((1,3), (4,2), (4,6), (6,5))
        print tester
        
        tester.deleteEdge(5,6)
        print tester
        
        print tester.degree(2), tester.degree(1)
        print tester.degreeFn()

        
    if enum==2:
        tester = Graph2([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])
        print tester
        
        tester.addEdge(5,2)
        print tester
        
        tester.deleteVertex(1)
        print(tester)
        
        tester.addEdges((1,3), (4,2), (4,6), (6,5))
        print tester
        
        tester.deleteEdge(5,6)
        print tester
        
        print tester.degree(2), tester.degree(1)
        print tester.degreeFn()
        
    if enum==3:
        tester = Graph1([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])
        print tester
        print tester.isConnected1(), tester.isConnected2()
        
        tester2 = Graph1([1,2,3,4,5,6], [(1,3), (4,5), (4,6), (3,2)])
        print tester2
        print tester2.isConnected1(), tester2.isConnected2()
        
    if enum==30:
        tester = Graph1([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])
        #print tester
        tester.isConnected1()
        
    if enum==31:
        tester = Graph1([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])        
        tester.isConnected2()
        
    if enum==32:
        tester2 = Graph1([1,2,3,4,5,6], [(1,3), (4,5), (4,6), (3,2)])
        tester2.isConnected1()
        
    if enum==33:
        tester2 = Graph1([1,2,3,4,5,6], [(1,3), (4,5), (4,6), (3,2)])
        tester2.isConnected2()
        
    if enum==4:
        tester = Graph2([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])
        print tester
        print tester.isConnected1(), tester.isConnected2()
                
        tester2 = Graph1([1,2,3,4,5,6], [(1,3), (4,5), (4,6), (3,2)])
        print tester2
        print tester2.isConnected1(), tester2.isConnected2()

        
    if enum==40:
        tester = Graph2([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])
        #print tester
        tester.isConnected1()
        
    if enum==41:
        tester = Graph2([1,2,3,4], [(1,2), (2,3), (2,4), (1,4)])        
        tester.isConnected2()
        
    if enum==42:
        tester2 = Graph2([1,2,3,4,5,6], [(1,3), (4,5), (4,6), (3,2)])
        tester2.isConnected1()
        
    if enum==43:
        tester2 = Graph2([1,2,3,4,5,6], [(1,3), (4,5), (4,6), (3,2)])
        tester2.isConnected2()
        
    if enum==5:
        tester = Graph1.random(12, 45)
        print tester
        print len(tester), len(tester.edges), tester.degreeFn()
        print tester.isConnected1()
        
    if enum==6:
        tester = Graph2.random(12, 45)
        print tester
        print len(tester), sum([tester.degree(v) for v in tester.graph]) / 2, tester.degreeFn()
        print tester.isConnected1()
        
    if enum==7:
        tester = Graph1.fromFile("graphExample.txt")
        print tester
        print len(tester), len(tester.edges), tester.degreeFn()
        print tester.isConnected1()
        
    if enum==8:
        tester = Graph2.fromFile("graphExample.txt")
        print tester
        print len(tester), sum([tester.degree(v) for v in tester.graph]) / 2, tester.degreeFn()
        print tester.isConnected1()

    if enum==9:
        tests = [Graph1.complete(5), Graph1.path(6), Graph1.cycle(8)]
        for gg in tests: 
            print gg
            
    if enum==10:
        tests = [Graph2.complete(5), Graph2.path(6), Graph2.cycle(8)]
        for gg in tests: 
            print gg
            
    if enum==11:
        test1 = Graph1([1,2,3,4,5], [(1,2), (2,3), (1,4), (2,5), (3,5)])
        test2 = Graph1([1,2,3,5,7], [(1,2), (1,7), (2,3), (2,7), (3,5), (5,7)])
        print test1, test2
        print Graph1.joinAtVert(test1, test2, 2, 7)
        
    if enum==12:
        test1 = Graph2([1,2,3,4,5], [(1,2), (2,3), (1,4), (2,5), (3,5)])
        test2 = Graph2([1,2,3,5,7], [(1,2), (1,7), (2,3), (2,7), (3,5), (5,7)])
        print test1, test2
        print Graph2.joinAtVert(test1, test2, 2, 7)

    if enum==13:
        tester = Graph1([1,2,3,4,5], [(1,2), (2,3), (1,4), (2,5), (3,5)])
        print tester
        print Graph1.collapseEdge(tester, 2, 5)
        
    if enum==14:
        tester = Graph2([1,2,3,4,5], [(1,2), (2,3), (1,4), (2,5), (3,5)])
        print tester
        print Graph2.collapseEdge(tester, 2, 5)


def timetest1(n=10):
    tester = Graph1.random(n, 4*n)
    tester.isConnected1()
    
def timetest2(n=10):
    tester = Graph1.random(n, 4*n)
    tester.isConnected2()
        
        
if __name__ == '__main__':
     import timeit
     x=[]
     y1=[]
     y2=[]
     
     for i in range(1,20):
         print i
         x.append(i)
         y1.append(timeit.timeit("timetest1("+str(10*i) + ")", setup="from __main__ import timetest1"))
         y2.append(timeit.timeit("timetest2("+str(10*i) + ")", setup="from __main__ import timetest2"))
#    print(timeit.timeit("test(41)", setup="from __main__ import test"))
#    print(timeit.timeit("test(42)", setup="from __main__ import test"))
#    print(timeit.timeit("test(43)", setup="from __main__ import test"))
    
    
     import matplotlib.pyplot as plt
    
     plt.plot(x, y1, 'ro', x, y2, 'b+')
     plt.show()