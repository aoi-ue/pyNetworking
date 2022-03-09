# Write down your name: Lian Yuhan
# Write down your student number: A0227161M

# from http import client
import httplib 
from socket import *
import sys

# port can be specified on command line. If omitted, it defaults to 12345
# you can also modify the code here to change the port if you do not want to
# use command line arguments
if len(sys.argv) > 1:
  serverPort = int(sys.argv[1])
else:
  serverPort = 12345

response200 = '200 OK\r\nDate: Wed, 23 Jan 2019 13:11:15 GMT\r\n\
Content-Length: 606\r\nContent-Type: text/html\r\n\r\n'

response404 = '404 Not Found\r\nContent-Length: 0\r\n\r\n'

response500 = '500 Server Error\r\nContent-Length: 0\r\n\r\n'

# Hint: refer to the socket programming solution
# program given in LumiNUS Files -> Lecture folder or Tutorial folder

# init server details 
SERVER_ADDRESS = (HOST, PORT) = 'localhost', serverPort
REQUEST_QUEUE_SIZE = 5

# Handle a request to the socket
def handle_request(client_connection):
    #read from request stream
    request = client_connection.recv(1024).decode('utf-8') 

    # Split request from spaces
    string_list = request.split('\r\n')
    header = string_list[0].split(' ')

    # connection = string_list[2][connection] = 'close'
    method = header[0] # First string is a method
    requesting_file = header[1] #Second string is request
    http_version = header[2] # third string is version

    # to inspect http request path in terminal 
    # print(string_list)
    print(method, requesting_file, http_version)
    
    if method == 'HEAD':
      # handle 200 
      if requesting_file == '/index.html': 
        client_connection.sendall(response200)
      # handle 404 with non-index.html file
      else: 
        client_connection.sendall(response404)
    else:
        client_connection.sendall(response500) 

    if http_version == 'HTTP/1.0': 
      string_list[2] = string_list[2].replace('keep-alive','close') 
      print(string_list)
      client_connection.close()

    if http_version == 'HTTP/1.1': 
      print("keep alive for future request")


def serve_forever():
    listen_sock = socket(AF_INET, SOCK_STREAM)
    # listen_sock.setdefaulttimeout(10)
    # socket.settimeout(10)
    listen_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listen_sock.bind(SERVER_ADDRESS)
    listen_sock.listen(REQUEST_QUEUE_SIZE) 
    # socket.settimeout(None)
    print('Serving HTTP on port {port}'.format(port=PORT))
    
    # try: 
    while True:
      # wait for the next connection and process it
      client_conn, _ = listen_sock.accept()
      handle_request(client_conn)
      client_conn.close()
    # except Exception as e:
    #   print("Time out!")
    
if __name__ == '__main__':
    serve_forever()