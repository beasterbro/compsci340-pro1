import socket 
import sys
exitCode = '400'
url = "www.example.com" #sys.argv[1]
PORT = 80
# STD out only gets body of response, not headers
# any other message goes to STD err
# listen and send over port 80


#gotta build HTTP stuff ourselve from header on down
response = ''
# with is easier try catch that auto closes sthings
# AF_INET is address protocol family
print(url)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # SOCK_STREAM specifies we are using TCP
    #s.bind((url, PORT))
    s.connect((url,PORT))
    #addr = s.getaddrinfo()
    req = "GET / HTTP/1.1\r\nHost:{}\r\n\r\n".format(url)
    s.send(req.encode('utf-8'))   
    # while True:
    #     window = s.recv(4096)
    #     if len(window) == 0:
    #         break
    # response += window
    response = s.recv(4096)
    print(response.decode())