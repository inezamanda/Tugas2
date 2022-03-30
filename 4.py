import socket
import ssl

PORT = 443
URL = "www.its.ac.id"

server_address = (URL, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = ssl.wrap_socket(client_socket, keyfile = None, certfile = None)
client_socket.connect(server_address)

request_header='GET / HTTP/1.0'
request_header+='\r\nHost: '+ URL
request_header+='\r\n\r\n'

client_socket.send(request_header.encode('utf-8'))

response = ''
while True:
    recv = client_socket.recv(1024)
    if not recv:
        break
    response += recv.decode('utf-8')

header = response.split('\r\n\r\n')[0]

contentTypeLine = header.split('Content-Type: ', 1)[1].split('\n')[0]
print('Content Type : ' + contentTypeLine.split(';')[1].split('=')[1])

client_socket.close()
