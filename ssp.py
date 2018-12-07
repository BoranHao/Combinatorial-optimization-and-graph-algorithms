#!usr/bin/env python
# -*- coding: utf-8 -*-

"""Apply the successive shortest path algorithm to solve the min-cost bipartite matching"""

import numpy as np
import copy


class Gra():
	"""Build the class to store networks. Add S and T points to convert the assignment into min-cost-max-flow"""

	def __init__(self, filename):
		self.flowgraph = {}
		self.lengraph = {}
		self.flow = {}
		self.maxflow = 0
		with open(filename) as f:
			line = f.readline()
			data = []
			while line:
				tp = line.split()
				data.append([int(i) for i in tp])
				line = f.readline()
			print(data)

		self.assi = {}

		self.Nnum = data[0][0]
		self.Sp = 0
		self.Ep = 2 * (self.Nnum + 1) - 1
		del data[0]
		for arc in data:
			self.flowgraph[(arc[0], arc[1] + self.Nnum)] = 1
			self.lengraph[(arc[0], arc[1] + self.Nnum)] = arc[2]
			self.flow[(arc[0], arc[1] + self.Nnum)] = 0

		self.floww = 0

		for j in range(self.Nnum):
			self.flowgraph[(0, j + 1)] = 1
			self.lengraph[(0, j + 1)] = 0
			self.flow[(0, j + 1)] = 0
			self.flowgraph[(j + 1 + self.Nnum, self.Ep)] = 1
			self.lengraph[(j + 1 + self.Nnum, self.Ep)] = 0
			self.flow[(j + 1 + self.Nnum, self.Ep)] = 0

		'''for i in range(self.Nnum):
			for j in range(self.Nnum,2*self.Nnum):
				# print((i+1,j+1))
				if (i+1,j+1) not in self.flowgraph.keys():
					self.flowgraph[(i+1,j+1)]=1
					self.lengraph[(i+1,j+1)]=1e4
					self.flow[(i+1,j+1)]=0'''

		# print(self.flowgraph)
		# print(self.lengraph)

		self.NN = self.Nnum
		self.Nnum = 2 * (self.Nnum + 1)

		self.NodePrice = np.zeros(self.Nnum, dtype=int)
		# print(self.NodePrice)

		self.orilen = copy.deepcopy(self.lengraph)
		self.rc = copy.deepcopy(self.lengraph)

	def GetPath(self):
		"""Regarding reduced cost as distance, find a shortest path from S to T using Dijkstra's algorithm. Update the node price and reduced cost"""
		self.tplen = copy.deepcopy(self.rc)

		for key in self.tplen:
			if key[1] == self.Nnum - 1:
				self.tplen[key] = 0

		D = {}
		for i in range(self.Nnum):
			D[i] = 1000
		D[self.Sp] = 0
		flag = 0

		pred = {}
		S = [0]

		while True:
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

		end = self.Ep
		path = [end]
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
		self.Augpath = Path  # found the shortest augmenting path

		print(self.Augpath)

		for i in range(self.Nnum):
			if abs(D[i]) < 40:
				self.NodePrice[i] += D[i]
			else:
				continue
				# self.NodePrice[i]+=D[i]/100

		print(self.NodePrice)

		for k in self.lengraph:
			'''if k in Path:
					self.lengraph[k]=0
			else:'''
			if k in self.rc.keys():
				self.rc[k] = self.lengraph[k] + \
					(self.NodePrice[k[0]] - self.NodePrice[k[1]])
			else:
				self.rc[(k[1], k[0])] = self.lengraph[k] + (self.NodePrice[k[0]
																		   ] - self.NodePrice[k[1]])  # renew reduced costs

		self.floww += self.orilen[self.Augpath[1]]

	def PushFlow(self):
		"""Push 1 unit flow along the augmenting path found"""
		ftp = []
		minf = 1
		self.maxflow += minf
		for arc in self.Augpath:
			self.rc[(arc[1], arc[0])] = -self.rc[arc]
			if arc[0] != 0 and arc[1] != self.Ep and arc[0] < arc[1]:
				self.assi[arc[0]] = arc[1]
		for arc in self.Augpath:
			del self.rc[arc]


def main():
	"""Path-push-path-push..."""
	# ob = Gra('medassign.txt')
	ob=Gra('smallassign.txt')

	while 1:
		try:
			ob.GetPath()
			ob.PushFlow()
			print(ob.floww)
		except BaseException:
			break

	print(sorted(ob.assi.keys()))
	print(sorted(ob.assi.values()))

	cost = 0
	for k in ob.assi:
		cost += ob.orilen[(k, ob.assi[k])]

	for k in ob.assi:
		if ob.assi[k] > ob.NN:
			ob.assi[k] -= ob.NN
	print(ob.assi)
	print(cost)


if __name__ == "__main__":
	main()
