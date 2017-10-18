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
    removeble_files = []
    list_of_file = extract_list_of_files(directory)
    for position, file in enumerate(list_of_file):
        file_name = list(file['name'])
        size = file['size']
        for position2, file in enumerate(list_of_file):
            file_name2 = list(file['name'])
            size2 = file['size']
            if (file_name == file_name2) and (size == size2) \
                    and (position2 > position):
                removeble_files.append(file['path'])
    for file_path in set(removeble_files):
        os.remove(file_path)
    return set(removeble_files)


def create_parser():
    parser = argparse.ArgumentParser(description='Remove duplicates')
    parser.add_argument("directory", help="path to checking folder")
    return parser

if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    for file_path in remove_duplicates(namespace.directory):
        print ("remove", file_path)
