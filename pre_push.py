#!usr/bin/env python
# -*- coding: utf-8 -*-

"""The preflow push algorithm by Goldberg and Tarjan"""

import numpy as np
import copy


class Gra():
    """Build the class to store the primal and residual networks"""

    def __init__(self, filename):
        with open(filename) as f:
            line = f.readline()
            data = []
            while line:
                tp = line.split()
                data.append([int(i) for i in tp])
                line = f.readline()

        self.Nnum = data[0][0]
        self.Sp = 0
        self.Ep = self.Nnum - 1
        self.flowgraph = np.zeros([self.Nnum, self.Nnum], dtype=int)
        self.residual = np.zeros([self.Nnum, self.Nnum], dtype=int)
        self.active = []
        self.flow = {}
        self.maxflow = 0

        del data[0]
        for arc in data:
            self.flowgraph[arc[0] - 1, arc[1] - 1] = arc[2]
            self.residual[arc[1] - 1, arc[0] - 1] = 0

        for i in range(300):
            for j in range(300):
                if self.flowgraph[i, j] > 0.01 and self.flowgraph[i, j] > 0.01:
                    print(i, j)
        self.origraph = copy.deepcopy(self.flowgraph)
        print(self.flowgraph)
        print(self.residual)

    def Pre(self):
        """Prepare. Initialize the height of nodes and active nodes"""
        self.H = np.zeros(self.Nnum, dtype=int)
        self.H[self.Sp] = self.Nnum
        self.E = np.zeros(self.Nnum, dtype=int)
        for i in range(self.Nnum):
            if self.flowgraph[self.Sp, i] != 0:
                self.E[i] = self.flowgraph[self.Sp, i]
                self.active.append(i)
                self.residual[i, self.Sp] = self.flowgraph[self.Sp, i]
        self.flowgraph = self.origraph - self.residual.T

    def Push(self):
        """Pick one active node and push the excess as much as possible"""
        flag = 0
        self.CurrAp = self.active[0]
        tpl = {}
        tpll = {}
        for j in range(self.Nnum):
            if self.flowgraph[self.CurrAp, j] > 0.001:
                tpl[(j, 1)] = self.flowgraph[self.CurrAp, j]
            if self.residual[self.CurrAp, j] > 0.001:
                tpl[(j, 2)] = self.residual[self.CurrAp, j]

        tdic = {}

        ff = 0
        while True:
            for n in tpl.keys():
                if self.H[n[0]] == self.H[self.CurrAp] - 1:
                    self.PushTarget = n[0]
                    self.typ = n[1]
                    ff = 1
                    break
            if ff == 1:
                break
            else:
                # Relabel. If fail to push, add the height until the excess can
                # be pushed
                self.H[self.CurrAp] += 1

        self.TargetH = self.H[self.PushTarget]

        flow = min([self.E[self.CurrAp], tpl[(self.PushTarget, self.typ)]])
        self.E[self.CurrAp] -= flow
        self.E[self.PushTarget] += flow
        if self.typ == 1:
            self.residual[self.PushTarget, self.CurrAp] += flow
            self.flowgraph[self.CurrAp, self.PushTarget] -= flow
        else:
            self.residual[self.CurrAp, self.PushTarget] -= flow
            self.flowgraph[self.PushTarget, self.CurrAp] += flow

        for j in range(self.Nnum):
            if self.E[j] != 0 and j not in self.active and j != self.Sp and j != self.Ep:
                self.active.append(j)

        if self.E[self.CurrAp] < 0.01:
            del self.active[0]
            flag = 1


def main():
    """Push-relabel-push-relabel..."""
    ob = Gra('medflow.txt')
    # ob=Gra('smallflow.txt')

    ob.Pre()
    while True:
        ob.Push()
        print(ob.E[0])
        if ob.active == []:
            for i in range(ob.Nnum):
                for j in range(ob.Nnum):
                    if ob.residual[j, i] > 0:
                        print((i, j))
                        print(ob.residual[j, i])
            print(ob.E)
            break


if __name__ == "__main__":
    main()
