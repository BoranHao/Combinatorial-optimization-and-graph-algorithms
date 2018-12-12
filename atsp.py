#!usr/bin/env python
# -*- coding: utf-8 -*-

"""Use shrinking cycle cover algorithm to solve asymmetric (metric) traveling salesman problem"""

import numpy as np
import copy
import scipy.io as sio
from my_euler import Euler


load_data = sio.loadmat('atsp.mat')
l3 = load_data['atsp']


class Gra():
    """To find the cycle cover, use SSC to solve a min-cost matching"""

    def __init__(self, filename):
        self.flowgraph = {}
        self.lengraph = {}
        self.flow = {}
        self.maxflow = 0

        self.assi = {}

        if filename == 'atsp.mat':
            load_data = sio.loadmat(filename)
            ll = load_data['atsp']

        else:
            ll = filename

        self.Nnum = len(list(ll))

        self.Sp = 0
        self.Ep = 2 * (self.Nnum + 1) - 1

        for i in range(1, self.Nnum + 1):
            for j in range(1, self.Nnum + 1):
                self.flowgraph[(i, j + self.Nnum)] = 1
                self.lengraph[(i, j + self.Nnum)] = ll[i - 1, j - 1]
                self.flow[(i, j + self.Nnum)] = 0

        # print(self.lengraph)

        self.floww = 0

        for j in range(self.Nnum):
            self.flowgraph[(0, j + 1)] = 1
            self.lengraph[(0, j + 1)] = 0
            self.flow[(0, j + 1)] = 0
            self.flowgraph[(j + 1 + self.Nnum, self.Ep)] = 1
            self.lengraph[(j + 1 + self.Nnum, self.Ep)] = 0
            self.flow[(j + 1 + self.Nnum, self.Ep)] = 0

        for i in range(self.Nnum):
            for j in range(self.Nnum, 2 * self.Nnum):
                # print((i+1,j+1))
                if (i + 1, j + 1) not in self.flowgraph.keys():
                    self.flowgraph[(i + 1, j + 1)] = 1
                    self.lengraph[(i + 1, j + 1)] = 1e5
                    self.flow[(i + 1, j + 1)] = 0

        self.NN = self.Nnum
        self.Nnum = 2 * (self.Nnum + 1)

        self.NodePrice = np.zeros(self.Nnum, dtype=int)
        # print(self.NodePrice)

        self.orilen = copy.deepcopy(self.lengraph)
        self.rc = copy.deepcopy(self.lengraph)

    def GetPath(self):
        """Find the shortest augmenting path using Dijkstra"""
        self.tplen = copy.deepcopy(self.rc)

        for key in self.tplen:
            if key[1] == self.Nnum - 1:
                self.tplen[key] = 0

        D = {}
        for i in range(self.Nnum):
            D[i] = 1e7
        D[self.Sp] = 0
        flag = 0

        pred = {}
        S = [0]

        while True:
            # print(len(S))
            if len(S) == self.Nnum:
                break
            for arc in self.tplen.keys():
                if arc[0] == flag and arc[1] not in S:
                    if D[flag] + self.tplen[arc] < D[arc[1]]:
                        D[arc[1]] = D[flag] + self.tplen[arc]
                        pred[arc[1]] = flag
            DD = D.copy()
            for key in S:
                del DD[key]
            flag = min(DD, key=DD.get)
            S.append(flag)
        # print(pred)
        # print(D)

        end = self.Ep
        # print(end)
        path = [end]
        # print(pred)
        while True:
            a = pred[end]
            path.append(a)
            if a == 0:
                break
            else:
                end = a
        path.reverse()
        Path = []
        for i in range(len(path) - 1):
            Path.append((path[i], path[i + 1]))
        self.Augpath = Path

        # print(self.Augpath)

        for i in range(self.Nnum):
            self.NodePrice[i] += D[i]

        # print(self.NodePrice)

        for k in self.lengraph:
            '''if k in Path:
                            self.lengraph[k]=0
            else:'''
            if k in self.rc.keys():
                self.rc[k] = self.lengraph[k] + \
                    (self.NodePrice[k[0]] - self.NodePrice[k[1]])
            else:
                self.rc[(k[1], k[0])] = self.lengraph[k] + \
                    (self.NodePrice[k[0]] - self.NodePrice[k[1]])

        # for flow in self.lengraph:
            # if self.lengraph[flow]<0.001:
                # print(str([flow[0],flow[1]])+' '+str(self.lengraph[flow]))

        # print(self.rc)

    def PushFlow(self):
        """Push flow along augmenting path found"""
        ftp = []
        minf = 1
        self.maxflow += minf
        for arc in self.Augpath:
            # self.flow[arc]+=minf
            # self.flowgraph[arc]-=minf

            self.rc[(arc[1], arc[0])] = -self.rc[arc]
            if arc[0] != 0 and arc[1] != self.Ep and arc[0] < arc[1]:
                self.assi[arc[0]] = arc[1]

        for arc in self.Augpath:
            del self.rc[arc]


def findcycle(dic):
    """Keep searching for cycles, until the graph is totally connected"""
    cycles = []
    dc = copy.deepcopy(dic)
    do = copy.deepcopy(dic)

    for k in dc:
        if dc[k] > 30:
            dc[k] -= 30
    print(dc)

    while True:
        cycle = []
        tpl = list(do.keys())
        if len(tpl) == 0:
            break

        node = tpl[0]
        while True:
            cycle.append(node)
            del do[node]
            node = dc[node]

            if node == cycle[0]:
                cycle.append(node)
                # print(cycle)
                break
        cycles.append(cycle)

    return cycles


def skip(ls):
    """Skip the repeated nodes in Euler path to find the final ATSP tour"""
    cost = 0
    tour = []
    record = []
    for n in ls:
        if n not in record:
            tour.append(n)
            record.append(n)
    tour.append(ls[0])
    print(tour)
    for i in range(len(tour) - 1):
        cost += l3[tour[i] - 1, tour[i + 1] - 1]
    print(cost)


def findpath(obj):
    """Use recursion to search the Euler path tree and obtain all paths"""
    fi = []
    for o in obj.next:

        flag = 0
        for i in o.po.values():
            if i != {}:
                flag = 1
                break
        if flag == 0:
            fi.append(o.no)
            while True:
                if o.back != []:
                    o = o.back
                    fi.append(o.no)
                else:
                    break
            fi.reverse()
            print(fi)
            skip(fi)
            break
        else:
            findpath(o)


def main():
    ob = Gra('atsp.mat')

    # f=np.array([[10000,1,2],[2,10000,1],[1,2,10000]])
    # ob=Gra(f)
    while True:
        try:
            ob.GetPath()
            ob.PushFlow()
        except BaseException:
            break

    for k in ob.assi:
        ob.floww += ob.orilen[(k, ob.assi[k])]

    Allarcs = []
    cyc = findcycle(ob.assi)
    print(cyc)

    for ls in cyc:
        for i in range(len(ls) - 1):
            Allarcs.append((ls[i], ls[i + 1]))

    while True:
        if len(cyc) == 1:
            break
        else:
            ptlist = []
            duiy = {}
            fduiy = {}
            for ls in cyc:
                ptlist.append(ls[0])
            print(ptlist)

            for i in range(len(ptlist)):
                duiy[i] = ptlist[i]
                fduiy[ptlist[i]] = i

            f = np.zeros([len(cyc), len(cyc)])
            for i in range(len(cyc)):
                for j in range(len(cyc)):
                    f[i, j] = l3[duiy[i] - 1, duiy[j] - 1]

            # f=np.array([[10000,1,2],[2,10000,1],[1,2,10000]])
            ob = Gra(f)
            while True:
                try:
                    # ma=input()
                    ob.GetPath()
                    ob.PushFlow()

                except BaseException:
                    break
            asi = ob.assi
            ndic = {}
            for k in asi:
                ndic[duiy[k - 1]] = duiy[asi[k] - len(cyc) - 1]

            print(ndic)
            cyc = findcycle(ndic)
            print(cyc)
            for ls in cyc:
                for i in range(len(ls) - 1):
                    Allarcs.append((ls[i], ls[i + 1]))

    arcs = Allarcs
    print(Allarcs)

    po = {}
    for arc in arcs:
        po[arc[0]] = {}
    for arc in arcs:
        po[arc[0]][arc[1]] = 0

    ob = Euler(2, po)
    print(ob.next)
    findpath(ob)


if __name__ == "__main__":
    main()
