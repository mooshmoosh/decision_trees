import numpy
import json
import random
import random_forest

class PredictedTextContainer(random_forest.DataContainer):
    """
    This is for building random forest that operate on text, but rather than
    predicting labels that are scattered throughout the data, the purpose
    is to predict the next character using the preceding text.
    """

    def __init__(self, filenames):
        # filenames is a list of all the files the data is in
        self.filenames = filenames
        with open('character_map.json', 'r') as f:
            self.character_map = json.loads(f.read())
        self.character_count = max(self.character_map.values())
        self.category_count = self.character_count + 1
        # The decision trees should be making their decisions using roughly
        # 10 characters of data.
        self.subvector_dimension = self.character_count * 10
        self.files = {}
        for file_index, filename in enumerate(self.filenames):
            with open(filename, 'r') as f:
                content = f.read()
                content_as_ints = [self.character_map.get(character, 0) for character in content]
                self.files[file_index] = {
                    'length': len(content),
                    'content': content_as_ints
                }
        self.last_dot_product = (None, None, None, None)

    def getFileLength(self, file_index):
        return self.files[file_index]['length']

    def generateRandomIdentifiers(self):
        """
        Return a list of identifiers that can be used with subVector to get
        a data point. In the case of text, they're the index of the filename
        in self.filenames, and the index of a character into the file.
        """
        result = []
        #sample_size = sum(self.getFileLength(index) for index in range(len(self.filenames)))
        # reducing the sample size for testing
        sample_size = 1000
        for _ in range(0, sample_size):
            file_index = random.randint(0, len(self.filenames) - 1)
            offset = random.randint(0, self.getFileLength(file_index))
            result.append((file_index, offset))
        result.sort(key=lambda x : x[0] * len(self.filenames) + offset)
        return result

    def subVector(self, identifier, coordinates):
        """
        Return the subvector of the datapoint identified by `identifier`
        containing `coordinates`.
        """
        vector = []
        file_id, offset = identifier
        for coordinate in coordinates:
            # The coordinate is an integer representing two values, the position
            # relative to offset, and
            coordinate_offset = offset - int(coordinate / self.character_count) - 1
            character_id = coordinate % self.character_count
            if coordinate_offset >= 0 and coordinate_offset < self.files[file_id]['length']:
                character_at_position = self.files[file_id]['content'][coordinate_offset]
                if character_at_position == character_id:
                    vector.append(1)
                else:
                    vector.append(0)
            else:
                vector.append(0)
        return vector

    def getCategory(self, identifier):
        """
        return the category that `identifier` is in.
        """
        file_id, offset = identifier
        if offset < 0 or offset >= self.files[file_id]['length']:
            return 0
        else:
            return self.files[file_id]['content'][offset]

    def getRandomCoordinates(self):
        """
        Calling this means that Data containers can implement their own distribution
        over coordinates. It also means that data containers can have theoretically
        infinite dimensional data.

        In the case of Text data the coordinate is somewhere randomly around
        the location the offset refers to. We use the geometric distribution
        so that the number is possibly infinite. It should be (on average)
        about 10 characters away, but 20 characters away is within 1 standard
        deviation.
        """
        return list(reversed(sorted(set(numpy.random.geometric(1 / (self.character_count * 10)) for _ in range(self.subvector_dimension)))))

    def dotProduct(self, identifier, coordinates, coeficients):
        if self.last_dot_product[0:3] == (identifier, coordinates, coeficients):
            return self.last_dot_product[3]
        result = 0
        file_id, offset = identifier
        file_length = self.files[file_id]['length']
        file_content = self.files[file_id]['content']
        offsets = [offset - int(coordinate / self.character_count) - 1 for coordinate in coordinates]
        character_ids = [coordinate % self.character_count for coordinate in coordinates]
        for index, coordinate_offset in enumerate(offsets):
            # The coordinate is an integer representing two values, the position
            # relative to offset, and
            if coordinate_offset >= 0 and coordinate_offset < file_length and file_content[coordinate_offset] == character_ids[index]:
                result += coeficients[index]
        self.last_dot_product = (identifier, coordinates, coeficients, result)
        return result

