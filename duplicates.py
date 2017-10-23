import os
from os.path import getsize
import argparse
from collections import defaultdict


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
    dict_same_files = defaultdict(set)
    removeble_files = {}
    for file in list_of_file:
        dict_same_files[(file['name'], file['size'])].add(file['path'])
    for key, value in dict_same_files.items():
        if len(value) > 1:
            removeble_files.update({key: value})
    return removeble_files


def create_parser():
    parser = argparse.ArgumentParser(description='Remove duplicates')
    parser.add_argument("directory", help="path to checking folder")
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    for (file, size), file_paths in remove_duplicates(args.directory).items():
        print("Find duplicated of {}\nSize is {}\nList same files:"
              .format(file, size), *file_paths)
