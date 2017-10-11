import os
from os.path import join, getsize
import argparse


def extract_list_of_files(directory,list_of_file = []):
    for dir_entry in os.scandir(directory):
        if dir_entry.is_dir():
           extract_list_of_files(dir_entry,list_of_file)
        else:
            list_of_file.append({dir_entry.name:{'size':getsize(dir_entry.path),'path':dir_entry.path}})
    os.scandir(directory).close()
    return  list_of_file

def remove_duplicates(directory):
    list_of_file = extract_list_of_files(directory)
    for position, file in enumerate(list_of_file):
        name = list(file.keys())[0]
        size = file[name]['size']
        for position2, file in enumerate(list_of_file):
            name2 = list(file.keys())[0]
            size2 = file[name2]['size']
            if (name == name2) and (size == size2) and (position2 > position):
                os.remove(file[name2]['path'])
                print ("remove ",file[name2]['path'])


def create_parser():
    parser = argparse.ArgumentParser(description= 'Remove duplicates')
    parser.add_argument("directory", nargs=1, help="path to checking folder")
    return parser

if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if namespace.directory:
        remove_duplicates(namespace.directory[0])
