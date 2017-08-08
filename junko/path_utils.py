#!/usr/bin/env python3

import os

def recursive_file_list(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        file_list += [os.path.join(root, file) for file in files]
    return file_list

def trim_path(header, path):
    if not header.endswith("/"):
        header = header + "/"
    if path.startswith(header):
        path = path[len(header):]
    return path

def trim_paths(header, paths):
    return [trim_path(header, path) for path in paths]

def recursive_trimmed_file_list(directory, header = None):
    header = header if header else directory
    file_list = recursive_file_list(directory)
    return trim_paths(header, file_list)
