import random
from BalancedSample import BalancedSample

class DecisionTree:
    def __init__(self, data):
        pass

def create_decision_trees(data, tree_count, output_pipe):
    random.seed()
    result = []
    sample = BalancedSample(data, data.getSmallestCategorySize())
    for tree_number in range(0, tree_count):
        sample.resample()
        result.append(DecisionTree(sample))
    output_pipe.send(result)
