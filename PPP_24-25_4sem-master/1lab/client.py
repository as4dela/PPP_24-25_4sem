import socket
import json

# Функция для отправки команды и получения текстового ответа
def send_command(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send(command.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    return response

# Функция для получения и отображения структуры директории
def get_and_display_structure():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send("GET_STRUCTURE".encode('utf-8'))

    # Получаем файл с сервера и сохраняем локально
    with open('structure.json', 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    client_socket.close()

    # Читаем и отображаем структуру
    with open('structure.json', 'r', encoding='utf-8') as f:
        structure = json.load(f)
        display_structure(structure)

# Функция для отображения структуры директории
def display_structure(structure, indent=0):
    for path, content in structure.items():
        print('  ' * indent + path)
        if 'directories' in content:
            for dir_name in content['directories']:
                print('  ' * (indent + 1) + dir_name + '/')
        if 'files' in content:
            for file_name in content['files']:
                print('  ' * (indent + 1) + file_name)