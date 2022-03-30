import socket
import ssl
from bs4 import BeautifulSoup

PORT = 443
URL = "classroom.its.ac.id"

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

body = response.split('\r\n\r\n')[1]

soup = BeautifulSoup(body, 'html.parser')
navbar = soup.find("ul", {"class": "navbar-nav"}).getText()
print(" ".join(navbar.split()))

client_socket.close()
