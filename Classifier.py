#!/usr/bin/python3

import numpy
import multiprocessing as mp
from DecisionTree import create_decision_trees
Vector = numpy.zeros

class Classifier:
    def __init__(self, category_count=2, process_count=2):
        self.category_count = category_count
        self.process_count = process_count

    def train(self, data, tree_count):
        processes = []
        for process_number in range(0, self.process_count):
            parent_pipe, child_pipe = mp.Pipe()
            new_process = mp.Process(
                target=create_decision_trees,
                args=(data, int(tree_count / self.process_count), child_pipe)
            )
            new_process.start()
            processes.append((parent_pipe, new_process))
        self.trees = []
        for pipe, process in processes:
            self.trees += pipe.recv()
            process.join()

    def evaluate(self, point):
        result = Vector(self.category_count)
        for tree in self.trees:
            result += tree.evaluate(point)
        return result

