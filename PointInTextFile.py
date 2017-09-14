from Vector import Vector
import os
import random

class PointInTextFile:
    def __init__(self, file_list, window_size, character_map):
        self.file_list = file_list
        self.category_count = len(file_list[0]['points'])
        self.character_map = character_map
        self.character_type_count = max(character_map.values())
        self.vector_size = (2 * window_size + 1) * self.character_type_count
        self.window_size = window_size

    def getRandomDataPoint(self, category_number):
        result = Vector(self.vector_size)
        random_file = random.choice(self.file_list)
        file_size = os.path.getsize(random_file['filename'])
        if category_number == 0:
            while random_position not in random_file['points']:
                random_position = random.randrange(0, file_size)
            start_point = max(0, random_position - window_size)
            first_coordinate = window_size - (random_position - start_point)
        else:
            start_point = max(0, random_file['points'][category_number - 1] - window_size)
            first_coordinate = window_size - (random_file['points'][category_number - 1] - start_point)

        with open(random_file['filename'], 'r') as f:
            f.seek(start_point)
            context = f.read(self.vector_size)
        for char in context:
            result[first_coordinate * self.character_type_count + self.character_map[char]] = 1
            first_coordinate += 1
        return result

