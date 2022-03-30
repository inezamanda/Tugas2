import socket
import ssl

PORT = 443
URL = "www.its.ac.id"

server_address = (URL, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = ssl.wrap_socket(client_socket, keyfile = None, certfile = None)
client_socket.connect(server_address)

request_header='GET / HTTP/1.0'
request_header+='\r\nAccept-Encoding: gzip'
request_header+='\r\nHost: '+ URL
request_header+='\r\n\r\n'

client_socket.send(request_header.encode())

file = open('a.gz', 'wb')
while True:
    recv = client_socket.recv(1024)
    file.write(recv)
    if not recv:
        break

currFile = open('a.gz', 'rb')
response = currFile.read()
header = response.split(b'\r\n\r\n')[0].decode()

encodeLine = header.split('Content-Encoding: ', 1)[1]
print('Content Encoding : ' + encodeLine.split('\n')[0])

client_socket.close()
