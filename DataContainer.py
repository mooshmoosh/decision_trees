import random

class DataContainer:
    def __init__(self, vector_size):
        self.category_count = 0
        self.vector_size = vector_size
        self.data_points = []

    def addDataPoint(self, category, vector):
        while category >= self.category_count:
            self.data_points.append([])
            self.category_count += 1
        self.data_points[category].append(vector)

    def getSmallestCategorySize(self):
        result = None
        for category in data_points:
            if result is None or len(self.data_points[category]) < result:
                result = len(category)
        return result

    def getRandomDataPoint(self, category_number):
        random_index = random.randrange(0, len(data_points[category_number]))
        return self.data_points[random_index]

    def getDataPoints(self):
        for category_number, category in enumerate(self.data_points):
            for data_point in category:
                yield data_point, category_number

