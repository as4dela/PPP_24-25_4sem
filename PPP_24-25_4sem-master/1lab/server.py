import os
import json
import struct
import socket
from pydub import AudioSegment
import tempfile

class AudioServer:
    def __init__(self, host='localhost', port=5000, audio_dir='audio_files'):
        self.host = host
        self.port = port
        self.audio_dir = audio_dir
        self.metadata_file = 'audio_metadata.json'
        self.metadata = {}
        
        # Создаем папку для аудио, если ее нет
        os.makedirs(self.audio_dir, exist_ok=True)
        self.generate_metadata()
        
        # Настройка сокета
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Сервер запущен на {self.host}:{self.port}")

    def generate_metadata(self):
        """Создает/обновляет файл метаданных"""
        self.metadata = {}
        for filename in os.listdir(self.audio_dir):
            if filename.lower().endswith(('.mp3', '.wav', '.ogg')):
                filepath = os.path.join(self.audio_dir, filename)
                try:
                    audio = AudioSegment.from_file(filepath)
                    self.metadata[filename] = {
                        'duration': len(audio) / 1000,  # в секундах
                        'format': os.path.splitext(filename)[1][1:]
                    }
                except Exception as e:
                    print(f"Ошибка обработки {filename}: {e}")
        
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)

    def handle_client(self, client_socket, addr):
        print(f"Подключен клиент: {addr}")
        try:
            while True:
                command = client_socket.recv(1024).decode().strip()
                if not command:
                    break

                if command == 'list':
                    # Отправляем список файлов
                    with open(self.metadata_file, 'rb') as f:
                        data = f.read()
                        client_socket.sendall(struct.pack('!I', len(data)))
                        client_socket.sendall(data)

                elif command.startswith('get'):
                    # Обработка запроса отрезка аудио
                    _, filename, start, end = command.split()
                    if filename not in self.metadata:
                        client_socket.sendall(struct.pack('!I', 0))
                        continue

                    filepath = os.path.join(self.audio_dir, filename)
                    audio = AudioSegment.from_file(filepath)
                    segment = audio[int(start)*1000 : int(end)*1000]
                    
                    with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp:
                        segment.export(tmp.name, format='mp3')
                        tmp.seek(0)
                        file_data = tmp.read()
                    
                    # Отправляем размер и данные
                    client_socket.sendall(struct.pack('!I', len(file_data)))
                    client_socket.sendall(file_data)

                else:
                    client_socket.send(b'Unknown command')

        except Exception as e:
            print(f"Ошибка с клиентом {addr}: {e}")
        finally:
            client_socket.close()
            print(f"Отключен клиент: {addr}")

    def run(self):
        while True:
            client_sock, addr = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(client_sock, addr)).start()

if __name__ == '__main__':
    server = AudioServer()
    server.run()    