import os
from os.path import join, getsize
import argparse


def extract_list_of_files(directory, list_of_file=None):
    if list_of_file is None:
        list_of_file = []
    for dir_entry in os.scandir(directory):
        if dir_entry.is_dir():
            extract_list_of_files(dir_entry, list_of_file)
        else:
            list_of_file.append({'name': dir_entry.name,
                                'size': getsize(dir_entry.path),
                                 'path': dir_entry.path})
    os.scandir(directory).close()
    return list_of_file


def remove_duplicates(directory):
    list_of_file = extract_list_of_files(directory)
    dict_same_files = {file['name']: [] for file in list_of_file}
    removeble_files = {}
    for position, file in enumerate(list_of_file):
        file_name = file['name']
        size = file['size']
        list_same_file = []
        for position2, file2 in enumerate(list_of_file):
            file_name2 = file2['name']
            size2 = file2['size']
            if (file_name == file_name2) and (size == size2) \
                    and (position2 > position):
                list_same_file.append(file['path'])
                list_same_file.append(file2['path'])
        if list_same_file != []:
            dict_same_files[file['name']] += list_same_file
            dict_same_files[file['name']] = \
                list(set(dict_same_files[file['name']]))
    for dict_key, dict_vaue in dict_same_files.items():
        if dict_vaue != []:
            removeble_files.update({dict_key: dict_vaue})
    return removeble_files


def create_parser():
    parser = argparse.ArgumentParser(description='Remove duplicates')
    parser.add_argument("directory", help="path to checking folder")
    return parser

if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    for file_name, file_paths \
            in remove_duplicates(namespace.directory).items():
        print("find duplicated of {}:".format(file_name), *file_paths)
