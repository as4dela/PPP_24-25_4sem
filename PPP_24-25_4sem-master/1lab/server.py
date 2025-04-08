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

# Функция для обработки подключения клиента
def handle_client(client_socket, addr):
    print(f"Подключен клиент: {addr}")
    while True:
        try:
            # Получаем данные от клиента
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Обработка команды установки новой корневой директории
            if data.startswith("SET_ROOT:"):
                new_root = data.split(":", 1)[1]
                if os.path.isdir(new_root):
                    structure = get_directory_structure(new_root)
                    save_structure_to_file(structure)
                    client_socket.send("Корневая директория обновлена".encode('utf-8'))
                else:
                    client_socket.send("Недопустимая директория".encode('utf-8'))

            # Обработка запроса на получение структуры
            elif data == "GET_STRUCTURE":
                with open('structure.json', 'rb') as f:
                    client_socket.sendfile(f)
            else:
                client_socket.send("Недопустимая команда".encode('utf-8'))
        except Exception as e:
            print(f"Ошибка: {e}")
            break
    client_socket.close()
    print(f"Отключен клиент: {addr}")

# Основная функция сервера
def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        # Запускаем обработку клиента в отдельном потоке
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()