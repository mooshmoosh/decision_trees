from Vector import Vector
import random

class BalancedSample:
    def __init__(self, data=None, sample_size=None):
        self.sample_size = sample_size
        if data is not None:
            self.data = data
            self.vector_size = data.vector_size
            self.sample_data = Vector((sample_size, self.vector_size))
            self.categories = Vector(sample_size)
            self.category_count = data.category_count

    def resample(self):
        for sample_index in range(0, self.sample_size):
            category = random.randrange(0, self.data.category_count)
            self.sample_data[sample_index] = data.getRandomDataPoint(category)
            self.categories[sample_index] = category

    def getSubSample(self, indicies):
        result = BalancedSample(sample_size=len(indicies))
        result.sample_size = len(indicies)
        result.vector_size = self.vector_size
        result.sample_data = Vector((self.sample_size, self.vector_size))
        result.categories = Vector(result.sample_size)
        result.category_count = self.category_count
        for i in range(0, len(indicies)):
            result.sample_data[i] = self.sample_data[indicies[i]]
            result.categories[i] = self.categories[indicies[i]]
        return result

    def isSingleClass(self):
        category = self.categories[0]
        for other in self.categories[1:]:
            if other != category:
                return False
        return True

    def getDataPoints(self):
        for index, data_point in enumerate(self.sample_data):
            yield data_point, self.categories[index]

