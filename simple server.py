import os
from http.server import BaseHTTPRequestHandler, HTTPServer

VIDEO_FILE = '/home/letquare/Downloads/1718888139_sample_960x400_ocean_with_audio.webm'
CHUNK_SIZE = 1024 * 1024  # Size of each chunk in bytes (1 MB)

class VideoHandler(BaseHTTPRequestHandler):
    chunks = []

    def do_GET(self):
        if self.chunks:
            chunk = self.chunks.pop(0)  # Получаем следующий чанк
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Content-Length', str(len(chunk)))
            self.end_headers()
            self.wfile.write(chunk)  # Отправляем чанк
        else:
            self.send_response(404)
            self.end_headers()

    @classmethod
    def load_chunks(cls, file_path):
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                cls.chunks.append(chunk)

def run(server_class=HTTPServer, handler_class=VideoHandler, port=8080):
    server_address = ('', port)
    handler_class.load_chunks(VIDEO_FILE)  # Загружаем чанки при старте сервера
    print(f'Starting server on port {port}...')
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
