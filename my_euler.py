#!usr/bin/env python
# -*- coding: utf-8 -*-

"""Given directed arcs, use recursion to find an Euler path"""

import copy


class Euler():
    """Define each node on the Euler path tree as a class object, connect nodes by store the predecessor"""

    def __init__(self, no, pos, last=[], pa=[], back=[]):
        self.no = no
        self.po = pos
        self.path = pa
        self.path.append(self.no)

        flag = 0

        for i in self.po.values():
            if i != {}:
                flag = 1
                break

        self.back = back
        self.next = []
        self.last = last
        self.walk()  # Once a node is built, search its successor to begin the recursion

    def walk(self):
        """Find all successors"""
        # print(self.po[self.no].keys())
        pat = copy.deepcopy(self.path)
        if len(self.po[self.no].keys()) != 0:
            # print(len(self.po[self.no].keys()))
            for n in self.po[self.no].keys():
                # print(n)
                poo = copy.deepcopy(self.po)
                del poo[self.no][n]
                # For each successor, keep building the node and searching...
                self.next.append(Euler(n, poo, self.no, pat, self))


def skip(ls):
    """Skip the repeated nodes in Euler path to find the final ATSP tour"""
    tour = []
    record = []
    for n in ls:
        if n not in record:
            tour.append(n)
            record.append(n)
    tour.append(ls[0])
    print(tour)


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


'''def main():
	# arcs = [(1, 2), (2, 3), (3, 1), (1, 5), (5, 4), (4, 5), (5, 6), (6, 8), (8, 7), (7, 6), (6, 1)]
	# arcs=[(1,2),(2,3),(3,2),(2,1)]

	po = {}
	for arc in arcs:
		po[arc[0]] = {}

	for arc in arcs:
		po[arc[0]][arc[1]] = 0
    ob = Euler(2)
    # print(ob.next)
    findpath(ob)


if __name__ == "__main__":
    main()'''
