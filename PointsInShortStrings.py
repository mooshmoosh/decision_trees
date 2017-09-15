from Vector import Vector
import os
import random
import shelve

class PointsInShortStrings:
    def __init__(self, db_filename, window_size=20, character_map={}):
        self.db_filename = db_filename
        try:
            self.string_count = self.getValue('__string_count')
            self.window_size = self.getValue('__window_size')
            self.character_map = self.getValue('__character_map')
            self.category_count = self.getValue('__category_count')
        except:
            db = shelve.open(self.db_filename, 'n')
            db.close()
            self.setValues([
                ['__string_count', 0],
                ['__window_size', window_size],
                ['__character_map', character_map]
            ])
        self.character_type_count = max(self.character_map.values())
        self.vector_size = (2 * self.window_size + 1) * self.character_type_count

    def setValue(self, key, value):
        with shelve.open(self.db_filename, 'w') as db:
            db[key] = value

    def setValues(self, data):
        with shelve.open(self.db_filename, 'w') as db:
            for [key, value] in data:
                db[key] = value

    def getValue(self, key):
        with shelve.open(self.db_filename, 'r') as db:
            return db[key]

    def addString(self, value, points):
        next_id = self.getValue('__string_count')
        self.setValues([
            [str(next_id), {"text": value, "points": points}],
            ["__string_count", next_id + 1]
        ])

    def getRandomDataPoint(self, category_number):
        result = Vector(self.vector_size)
        random_file = self.getValue(str(random.randrange(0, self.string_count)))
        file_size = len(random_file['text'])
        if category_number == 0:
            while random_position not in random_file['points']:
                random_position = random.randrange(0, file_size)
            start_point = max(0, random_position - window_size)
            first_coordinate = window_size - (random_position - start_point)
        else:
            start_point = max(0, random_file['points'][category_number - 1] - window_size)
            first_coordinate = window_size - (random_file['points'][category_number - 1] - start_point)
        end_point = start_point + len(random_file['text'])
        context = random_file['text'][start_point:end_point]
        for char in context:
            result[first_coordinate * self.character_type_count + self.character_map.get(char, 0)] = 1
            first_coordinate += 1
        return result

