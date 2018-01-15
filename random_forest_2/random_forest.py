from collections import namedtuple
import random

DecisionNode = namedtuple('DecisionNode', ['final', 'threshold', 'above', 'below', 'result'])

class DataPoint:
    def __init__(self, identifier, data):
        self.data = data
        self.identifier = identifier

    def __getitem__(self, coordinate):
        return self.data.subVector(self.identifier, coordinate)

class DataSample:
    def __init__(self, data, identifiers):
        self.category_count = data.category_count
        self.identifiers = identifiers
        self.data = data
        self.subvector_dimension = data.subvector_dimension

    def subVectors(self, coordinates):
        """
        return a generator of data_point, category tuples. Each data_point
        only contains the coordinates from the real data point specified
        in coordinates.
        """
        for identifier in self.identifiers:
            yield self.data.subVector(identifier, coordinates)

    def getRandomCoordinate(self):
        return self.data.getRandomCoordinate():

    def singleCategory(self):
        result = None
        for data_point, category in self.subVectors([]):
            if category is None:
                result = category
            if category != result:
                return False, None
        return True, result

    def split(self, split_function):
        """
        return a tuple of two data samples. The first contains the datapoints
        for which split_function returned true, the second contains the rest.
        """
        true_points = []
        false_points = []
        for identifier in self.identifiers:
            if split_function(DataPoint(identifier, self.data)):
                true_points.append(identifier)
            else:
                false_points.append(identifier)
        return DataSample(self.data, true_points), DataSample(self.data, false_points)

class DataContainer:
    """
    This class is where you abstract away the nitty gritty details of the
    data. The data may be stored in an efficient way on disk, but this class
    exposes the data as high dimensional vectors.
    """

    def __init__(self):
        self.category_count = 0

    def randomSample(self):
        return DataSample(self, self.generateRandomIdentifiers())

    def generateRandomIdentifiers(self):
        """
        Return a list of identifiers that can be used with subVector to get
        a data point. The identifiers can be anything, but ideally they're
        small and efficient. If the data is text spread over many files,
        they may be an index into a list of files, and an index into the
        file itself. If the data is just vectors of numbers they could just
        be a line number in a csv file.
        """
        return []

    def subVector(self, identifier, coordinates):
        """
        Return the subvector of the datapoint identified by `identifier`
        containing `coordinates`.
        """
        return [0] * len(coordinates), None

    def getRandomCoordinate(self):
        """
        Calling this means that Data containers can implement their own distribution
        over coordinates. It also means that data containers can have theoretically
        infinite dimensional data.
        """
        return 0

def compute_gini_impurity(category_counts):
    result = 0
    total = 0
    for category_count in category_counts:
        result += category_count ** 2
        total += category_count
    return 1 - (result / (category_count ** 2))

def dot_product(data_point, coordinates, coeficients):
    result = 0
    for index, coordinate in enumerate(coodinates):
        result += x[coordinate] * coeficients[index]
    return result

def construct_random_decision_tree(sample, possible_split_count):
    all_in_one_category, category = sample.singleCategory()
    if all_in_one_category:
        return DecisionNode(
            final=True,
            result=category,
            threshold=None,
            above=None,
            below=None
        )
    overall_lowest_gini_impurity = 1
    for _ in range(0, possible_split_count):
        coordinates = list(set([sample.getRandomCoordinate() for _ in range(sample.subvector_dimension )]))
        coeficients = [random.random() for _ in range(len(coordinates))]
        decision_values = []
        for each data point calculate the dot product of the selected coordinates with the weights
        for data_point, category in sample.subVectors(coordinates):
            decision_values.append((dot_product(data_point, coordinates, coeficients), category))
        category_counts = [0] * sample.category_count
        decision_values.sort(key=lambda x : x[0])
        lowest_gini_impurity = 1 # gini impurity is always less than 1
        for decision_value, category  in decision_values:
            category_counts[decision_value[1]] += 1
            gini_impurity = compute_gini_impurity(category_counts)
            if gini_impurity < lowest_gini_impurity:
                lowest_gini_impurity = gini_impurity
                best_split = decision_value[0]
        if lowest_gini_impurity <= overall_lowest_gini_impurity:
            overall_lowest_gini_impurity = lowest_gini_impurity
            overall_best_split = best_split
            best_coordinates = coordinates
            best_coefficients = coeficients
    above_sample, below_sample = sample.split(lambda x : dot_product(x, best_coordinates, best_coefficients) > overall_best_split)
    return DecisionNode(
        final=False,
        threshold = best_split,
        above=construct_random_decision_tree(above_sample),
        below=construct_random_decision_tree(below_sample),
        result=None)

class DecisionTree:
    def __init__(self, sample, possible_split_count):
        self.root = construct_random_decision_tree(sample, possible_split_count)

    def evaluate(self, inputs):
        step = self.root
        while not step.final:
            if inputs[step.coordinate] > step.threshold:
                step = step.above
            else:
                step = step.below
        return step.result

class RandomForest:
    def __init__(self):
        self.trees = []
        self.category_count = 0

    def evaluate(self, inputs):
        result = [0] * self.category_count
        for tree in self.trees:
            result[tree.evaluate(inputs)] += 1
        for index in range(0, self.category_count):
            result[index] /= len(self.trees)
        return result

    def train(self, data):
        self.category_count = data.category_count
        self.trees = []
        for index in range(0, self.tree_count):
            self.trees.append(DecisionTree(data.randomSample()), 5)