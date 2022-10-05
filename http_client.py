from socket import socket

exitCode = '400'
url = ''
PORT = 80
# STD out only gets body of response, not headers
# any other message goes to STD err
# listen and send over port 80


def __init__(self, url):
    self.url = url
    # with is easier try catch that auto closes sthings
    # AF_INET is address protocol family
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # SOCK_STREAM specifies we are using TCP
        s.connect((url, self.PORT))
        s.sendall('GET')
        data = s.recv(1024)
