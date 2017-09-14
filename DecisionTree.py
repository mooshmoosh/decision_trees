import random
from BalancedSample import BalancedSample
from Vector import Vector

class LeafNode:
    def __init__(self, sample):
        self.result = Vector(sample.vector_size)
        for data_point, category in sample.getDataPoints():
            self.result[category] = 1
            break

    def evaluate(self, vector):
        return self.result

class DecisionTree:
    def __init__(self, sample):
        self.weights = Vector(sample.sample_size)
        for index in len(self.weights):
            self.weights[index] = random.random()
        # result has 3 columns.
        #   - the projection of the data point in the
        #     direction the decision tree cares about
        #   - the category it belongs to
        #   - the index into the sample of the point
        result = Vector((sample.sample_size, 3))
        index = 0
        for data_point, category in sample.getDataPoints():
            result[index][0] = self.weights.dot(data_point)
            result[index][1] = category
            result[index][2] = index
            index += 1
        # This sorts the results by the first column
        result.sortBy(0)
        # Next find the "cut off" value of the projection that gives
        # the best separation of the data. We do this by iterating over
        # result, and counting how many data points are in each
        # category. The measure of fit is then the gini impurity of the
        # set of points in the set with projection less than the cutoff.
        # For simplicity We actually use 1 - gini_impurity and maximise
        # it instead of minimising real gini impurity
        category_counts = Vector(sample.category_count)
        best_gini = 0
        best_cutoff = None
        cutoff_index = None
        for index in range(0, len(result) - 1):
            category_counts[result[index][1]] += 1
            gini_impurity = 0
            for category in range(0, len(category_counts)):
                gini_impurity += (category_counts[category] / (index + 1)) ** 2
            if gini_impurity > best_gini:
                best_cutoff = (result[index][0] + result[index + 1][0]) / 2
                best_gini = gini_impurity
                cutoff_index = index
        self.cutoff = best_cutoff

        next_sample = sample.getSubSample(result.column(2)[0:cutoff_index + 1])
        if next_sample.isSingleClass():
            self.left_tree = LeafNode(next_sample)
        else:
            self.left_tree = DecisionTree(next_sample)

        next_sample = sample.getSubSample(result.column(2)[cutoff_index + 1:])
        if next_sample.isSingleClass():
            self.right_tree = LeafNode(next_sample)
        else:
            self.right_tree = DecisionTree(next_sample)

    def evaluate(self, vector):
        projection = self.weights.dot(data_point)
        if projection < self.cutoff:
            return self.left_tree.evaluate(vector)
        else:
            return self.right_tree.evaluate(vector)

def create_decision_trees(data, tree_count, output_pipe):
    random.seed()
    result = []
    sample = BalancedSample(data, 10000)
    for tree_number in range(0, tree_count):
        sample.resample()
        result.append(DecisionTree(sample))
    output_pipe.send(result)

