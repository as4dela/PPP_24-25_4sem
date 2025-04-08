import os
import json
import socket
import threading

# Функция для рекурсивного получения структуры директории
def get_directory_structure(root_dir):
    structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_path = os.path.relpath(dirpath, root_dir)
        if relative_path == '.':
            relative_path = ''
        structure[relative_path] = {
            'directories': dirnames,
            'files': filenames
        }
    return structure

# Функция для сохранения структуры в JSON-файл
def save_structure_to_file(structure, filename='structure.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=4)