from PointInTextFile import PointInTextFile

class DataLoadError(Exception):
    def __init__(self, message):
        self.message = message

def SubStringsInFiles(file_list, window_size, character_map):
    new_file_list = []
    for example_file in file_list:
        with open(example_file['filename'], 'r') as f:
            example_content = f.read()
        new_file = {
            'filename': example_file['filename'],
            'points': []
        }
        for substring in example_file['substrings']
            if 'occurance' in substring:
                occurance_number = 1
                start_index = -1
                while occurance_number <= substring['occurance']:
                    start_index = example_content.index(substring['value'], start_index + 1)
                    occurance_number += 1
                end_index = start_index + len(substring['value'])
            else:
                start_index = example_content.index(substring['value'])
                end_index = start_index + len(substring['value'])
                if substring['value'] in example_content[end_index:]:
                    raise DataLoadError('substring {subs} occurred multiple times, but occurance was not specified'.format(subs=substring['value']))
            new_file['points'] += [start_index, end_index]
        new_file_list.append(new_file)
    return PointInTextFile(new_file_list, window_size, character_map)

