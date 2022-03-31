from urllib.parse import unquote
import socket
import configparser
import threading
import os

config = configparser.RawConfigParser()
cfg_path = 'no6/httpserver.conf'
config.read(cfg_path)

server_address = (config.get('server-config', 'server'), int(config.get('server-config', 'port')))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)

DATASET = 'no6/dataset'

def listFiles():
    message = ""
    for file in os.listdir(os.getcwd()+ '/dataset'):
        message += f"<li><h5><a href='/{file}'>{file}</a></h3></li>\n"
    return message

def handle_client(conn, addr):
    print(f"Connection {addr} connected.")

    connected = True
    while connected:
      data = conn.recv(4096).decode('utf-8')
      
      request_header = data.split('\r\n')
      request_file = request_header[0].split()[1]
      request_file = unquote(request_file)
      print("request file: ", request_file)
      response_header = b''
      response_data = b''
      
      if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
        f = open('no6/index.html', 'r')
        response_data = f.read()
        f.close()
        
        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
          + str(content_length) + '\r\n\r\n'

        conn.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

      elif (request_file == '/dataset' or request_file == 'dataset'):
        response_data = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h1>
                DATASET
            <h1>
            <ul>
        '''
        response_data += listFiles()
        response_data += '''
            <ul>
        </body>
        </html>
        '''

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
          + str(content_length) + '\r\n\r\n'
        
        conn.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

      elif request_file.strip('/') in os.listdir(os.getcwd() + '/dataset'):
        filename = request_file.strip('/')
        print("filename : ", filename)

        extension = request_file.split('.')[1]
        extension = '.' + extension
        print("extension : ", extension)

        with open(f'{os.getcwd()}/dataset/' + filename, 'rb') as file:
            response_data = file.read()

        content_length = len(response_data)
        response_header = f'HTTP/1.1 200 OK\r\nContent-Disposition: attachment; filename="{filename}{extension}"\r\nContent-Type: application/octet-stream; charset=UTF-8\r\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
        conn.sendall(response_header.encode('utf-8') + response_data)           
        
      else:
        f = open('no6/404.html', 'r')
        response_data = f.read()
        f.close()
          
        content_length = len(response_data)
        response_header = 'HTTP/1.1 404 Not found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'

        conn.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

    conn.close()
        

def start():
    server_socket.listen()
    print("Host :" + config.get('server-config', 'server'))
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("start server...")
start()