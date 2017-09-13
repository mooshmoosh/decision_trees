import numpy
Vector = numpy.zeros

class BalancedSample:
    def __init__(self, data, sample_size):
        self.data = data
        self.sample_size = sample_size
        self.categories = Vector((data.category_count, sample_size, data.vector_size))

    def resample(self):
        for category in range(0, self.data.category_count):
            for sample_index in range(0, self.sample_size):
                self.categories[category][sample_index] = data.getRandomDataPoint(category)


