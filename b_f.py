#!usr/bin/env python
# -*- coding: utf-8 -*-

"""Bellman-Ford shortest path algorithm"""

import time


def main():
    pred = {}
    D = {}
    arcs = {}
    Q = [1]
    data = []

    # with open('smallnet.txt') as f:
    # with open('largenet.txt') as f:
    with open('verylargenet.txt') as f:
        line = f.readline()
        while line:
            tp = line.split()
            data.append([int(i) for i in tp])
            line = f.readline()

    Nnum = data[0][0]
    del data[0]
    for ls in data:
        arcs[(ls[0], ls[1])] = ls[2]

    for i in range(Nnum):
        D[i + 1] = 1e19
    D[1] = 0
    flag = 1

    begin = time.time()
    while True:
        if len(Q) == 0:
            break
        flag = Q[0]
        for arc in arcs.keys():
            if arc[0] == flag:
                if D[flag] + arcs[arc] < D[arc[1]]:
                    # update the shortest distance using dynamic programming
                    # idea
                    D[arc[1]] = D[flag] + arcs[arc]
                    pred[arc[1]] = flag
                    if arc[1] not in Q:
                        Q.append(arc[1])
        del Q[0]

    over = time.time()
    print('Run Time', over - begin, '\n')

    report = [1000, 250, 1500]
    for end in report:
        print('Node', end)
        print('Shortest Path Length:', D[end])
        path = [end]
        while True:
            a = pred[end]  # Get the path from the end using predecessors
            path.append(a)
            if a == 1:
                break
            else:
                end = a
        path.reverse()
        print('Shortest Path', path, '\n')

    print('Sum of Shortest distance', sum(D.values()))


if __name__ == "__main__":
    main()
