import numpy

class Vector:
    def __init__(self, dimension):
        self.vector = numpy.zeros(dimension)

    def __setitem__(self, index, value):
        self.vector[index] = value

    def __getitem__(self, index):
        return self.vector[index]

    def sortBy(self, column):
        self.vector = self.vector[self.vector[:,column].argsort()]

    def dot(self, other):
        if isinstance(other, Vector):
            return numpy.matmul(self.vector, numpy.transpose(other.vector))
        else:
            return numpy.matmul(self.vector, numpy.transpose(other))

    def column(self, column):
        return self.vector[:,column]

    def __len__(self):
        return len(self.vector)
