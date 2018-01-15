import numpy
import json
import random
import random_forest

class TextDataContainer(random_forest.DataContainer):
    def __init__(self, offsets):
        # filenames is a list of all the files the data is in
        self.filenames = []
        self.categories = []
        self.data_by_label = {}
        self.data_by_offset = {}
        self.category_count = 0
        with open('character_map.json', 'r') as f:
            self.character_map = json.loads(f.read())
        self.character_count = max(self.character_map.values())
        # The decision trees should be making their decisions using roughly
        # 10 characters of data.
        self.subvector_dimension = self.character_count * 10
        # offsets is a list of tuples of the form (filename, offset, label).
        # filename is the filename being labeled. offset is the offset into
        # the file where the label is, and label is the string for the label.
        for (filename, offset, label) in offsets:
            if filename not in self.filenames:
                self.filenames.append(filename)
            if label not in self.categories:
                self.categories.append(label)
                self.data_by_label[label] = [(self.filenames.index(filename), self.category_count)]
                self.category_count += 1
            else:
                self.data_by_label[label].append((self.filenames.index(filename), self.categories.index(label)))
            self.data_by_offset[(self.filenames.index(filename), offset)] = self.categories.index(label)
        # We add one to the category count for the category of offsets that
        # are unlabelled.
        self.category_count += 1
        self.files = {}

    def getFilenameLength(self, file_index)
        if file_index not in self.files:
            self.loadFile(file_index)
        return self.files[file_index]['length']

    def loadFile(self, file_index):
        with open(self.filenames[file_index], 'r') as f:
            content = f.read()
            self.files[file_index] = {
                'length': len(content),
                'content': content
            }

    def generateRandomIdentifiers(self):
        """
        Return a list of identifiers that can be used with subVector to get
        a data point. In the case of text, they're the index of the filename
        in self.filenames, and the index of a character into the file.

        We want all the categories to be equally likely to be chosen in our
        random sample. This includes the implicit "unlabelled" category.
        """
        result = []
        sample_size = len(self.data_by_offset) * self.category_count / (self.category_count - 1)
        for _ in range(0, sample_size):
            category = random.randint(0, self.category_count)
            if category < self.category_count - 1:
                result.append(random.choice(self.data_by_label[self.categories[category]]))
            else:
                while True:
                    file_index = random.randint(0, len(self.filenames))
                    offset = random.randint(0, self.getFilenameLength(file_index))
                    if (file_index, offset) not in self.data_by_offset:
                        break
                result.append((file_index, offset))
        return result

    def subVector(self, identifier, coordinates):
        """
        Return the subvector of the datapoint identified by `identifier`
        containing `coordinates`.
        """
        vector = []
        file_id, offset = identifier
        if file_id not in self.files:
            self.loadFile(file_id)
        for coordinate in coordinates:
            # The coordinate is an integer representing two values, the position
            # relative to offset, and
            relative_position = int(coordinate / self.character_count)
            elif relative_position % 2 == 0:
                # relative position is negative ( or zero)
                relative_position = offset - relative_position / 2
            else:
                # relative position is positive
                relative_position = offset - (relative_position + 1) / 2
            character_id = coordinate % self.character_count
            if coordinate_offset >= 0 and coordinate_offset < self.files[file_id]['length']:
                character = self.files[file_id]['content'][coordinate_offset]
                if character not in self.character_map and character_id == 0:
                    vector.append(1)
                elif character in self.character_map and character_id == self.character_map[character]:
                    vector.append(1)
                else:
                    vector.append(0)
            else:
                vector.append(0)
        return vector

    def getRandomCoordinate(self):
        """
        Calling this means that Data containers can implement their own distribution
        over coordinates. It also means that data containers can have theoretically
        infinite dimensional data.

        In the case of Text data the coordinate is somewhere randomly around
        the location the offset refers to. We use the geometric distribution
        so that the number is possibly infinite. It should be (on average)
        about 5 characters away, but 10 characters away is within 1 standard
        deviation.
        """
        return numpy.random.geometric(1 / (self.character_count * 5))
