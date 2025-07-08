import copy

import networkx as nx

from database.DAO import DAO
from model.circuit import Circuit


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestSol = []
        self._maxScore = 0

    def getYears(self):
        return DAO.getYears()

    def buildGraph(self, year1, year2):
        self._graph.clear()
        self._idMap = {}

        nodes = DAO.getAllCircuits()
        for n in nodes:
            self._idMap[n.circuitId] = n
            self._addRisultati(n, year1, year2)
        self._graph.add_nodes_from(nodes)

        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u.circuitId < v.circuitId:
                    peso = self._calcolaPesoArco(u, v)
                    if peso > 0:
                        self._graph.add_edge(u, v, weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def _addRisultati(self, nodo:Circuit, year1, year2):
        risultatiCircuito = DAO.getRisultatiCircuito(nodo.circuitId, year1, year2)
        for row in risultatiCircuito:
            if row[0] not in nodo.risultati.keys():
                nodo.risultati[row[0]] = [row[1]]
            else:
                nodo.risultati[row[0]].append(row[1])

    def _calcolaPesoArco(self, u:Circuit, v:Circuit):
        peso = 0

        if len(u.risultati.keys()) == 0 or len(v.risultati.keys()) == 0:
            return peso

        for year in u.risultati.keys():
            for p in u.risultati[year]:
                if p.time:
                    peso += 1

        for year in v.risultati.keys():
            for p in v.risultati[year]:
                if p.time:
                    peso += 1
        return peso


    def getComponenteConnessa(self):
        return sorted(list(max(nx. connected_components(self._graph), key=len)), key = lambda x:self.getPesoMinimo(x), reverse=True)

    def getPesoMinimo(self, node:Circuit):
        pesoMinimo = 100000000
        for edge in self._graph.edges(node, data=True):
            if edge[2]["weight"] < pesoMinimo:
                pesoMinimo = edge[2]["weight"]
        return pesoMinimo


    def getBestCampionato(self, K, M):
        self._bestSol = []
        self._maxScore = 0

        circuiti = self.getComponenteConnessa()
        for c in circuiti:
            if len(c.risultati.keys()) >= M:
                self._ricorsione([c], circuiti, K, M)

        return self._bestSol, self._maxScore

    def _ricorsione(self, parziale, circuiti, K, M):
        if len(parziale) == K:
            if (score:=self._calcolaScore(parziale)) > self._maxScore:
                self._bestSol = copy.deepcopy(parziale)
                self._maxScore = score
        else:
            for c in circuiti:
                if c not in parziale:
                    if len(c.risultati.keys()) >= M:
                        parziale.append(c)
                        self._ricorsione(parziale, circuiti, K, M)
                        parziale.pop()

    def _calcolaScore(self, soluzione):
        score = 0
        for c in soluzione:
            nP = 0
            nPtot = 0
            for year in c.risultati.keys():
                for p in c.risultati[year]:
                    nPtot += 1
                    if p.time:
                        nP += 1
            score += 1 - nP/nPtot
        return score
