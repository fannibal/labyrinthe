import sys
import numpy as np
import time

def isEmpty(dictionary):
    for element in dictionary:
        if element:
            return True
    return False

class Vertex(object):
    '''
    Classe representant les sommets
    '''

    '''
    Variables de classe pour les couleurs de marquage
    '''
    WHITE = 0
    GREY = 1
    BLACK = 2

    def __init__(self,label, distance=0):
        '''
        Constructeur
        '''
        self.label = label # nom du sommet
        self.distance = distance #distance du sommet a l'origine
        self.adjList = [] #liste d'adjacence
        self.mark = Vertex.WHITE # marque

    def __lt__(self, v):
        '''
        teste si le sommet est < a un autre sommet
        '''
        return self.distance < v.distance

    def __gt__(self, v):
        '''
        teste si le sommet est > a un autre sommet
        '''
        return self.distance > v.distance

    def __str__(self):
        return str(self.label)+'('+str(self.distance)+')'

    def __repr__(self):
        return str(self.label)+'('+str(self.distance)+')'

    def full_repr(self):
        '''
        Representation complete : sommet + voisins
        '''
        return str(self.label)+'('+str(self.distance)+') -> '+str(self.adjList)

    def addNeighbor(self, v, w):
        '''
        Ajoute un voisin au sommet
        '''
        self.adjList.append(Edge(v, w))

class Edge(object):
    '''
    Classe representant les arcs
    '''
    def __init__(self, neigh, w):
        self.neighbor = neigh
        self.weight = w

    def __repr__(self):
        return '--{'+str(self.weight)+'}-->'+str(self.neighbor.label)


class PrioQueue(object):
    '''
    File de priorite
    '''
    def __init__(self):
        self._queue = []

    def offer(self, v):
        '''
        Ajoute un sommet a la file
        '''
        self._queue.append(v)

    def poll(self):
        '''
        Extrait le sommet de valeur minimale de la file
        '''
        x = min(self._queue)
        self._queue.remove(x)
        return x

    def size(self):
        '''
        Nombre d'elements de la file
        '''
        return len(self._queue)

    def __str__(self):
        return str(self._queue)

class Graph(object):
    '''
    Graphe represente par une liste de sommets
    '''
    def __init__(self):
        self._vertices = []

    def addVertex(self, v):
        self._vertices.append(v)

    def addEdge(self, source, dest, weight):
        source.addNeighbor(dest, weight)

    def read(self, filename):
        '''
        Initialisation du graphe par lecture de fichier
        '''
        f = open(filename, 'r')
        for i in range(int(f.readline())):
            self.addVertex(Vertex(i))
        while True:
            t=list(map(lambda x: float(x), f.readline().strip().split()))
            if len(t)<3:
                break
            s=self._vertices[int(t[0])]
            d=self._vertices[int(t[1])]
            self.addEdge(s, d, t[2])
        f.close()


    def print_graph(self):
        '''
        Affichage du graphe
        '''
        for v in self._vertices:
            print('['+v.full_repr()+']')
        print()

    def print_pred(self, pi):
        '''
        Affichage des predecesseurs
        pi doit faire la meme taille que self._vertices
        '''
        for v in self._vertices:
            print('['+str(v)+' <- '+str(pi[v.label])+']')

    def __str__(self):
        return str(self._vertices)


    def dijkstra(self, n_init=0):
        '''
        Plus court chemin par l'algorithme de Dijkstra
        n_init : numero du sommet initial
        '''
        pi    = dict() # Dictionnaire de predecesseurs
        prio  = PrioQueue() #file de priorite
        init  = self._vertices[n_init] #sommet de depart

        for vertex in self._vertices:
            vertex.distance = np.inf
        init.distance = 0

        for vertex in self._vertices:
            prio.offer(vertex)

        while isEmpty(prio._queue):
            u = prio.poll()
            for edge in u.adjList:
                w = edge.weight
                newLen = u.distance + w
                if newLen < edge.neighbor.distance:
                    edge.neighbor.distance = newLen
                    prio.offer(edge.neighbor)
                    pi["{}".format(edge.neighbor)] = u
        #print(len(pi), len(self._vertices))
        return pi
