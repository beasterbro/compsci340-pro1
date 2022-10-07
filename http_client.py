import socket
import sys
from webbrowser import get

from requests import head

exitCode = '400'
URL = sys.argv[1]  # sys.argv[1]
PORT = 80
# STD out only gets body of response, not headers
# any other message goes to STD err
# listen and send over port 80

# gotta build HTTP stuff ourselves from header on down
response = ''


def getHeader(resp):
    return resp.split('<!')[0]


def getBody(resp):
    return '<!' + resp.split('<!')[1]


def getUrl(header):
    return header.split('Location: ')[1].split(' ')[0].split('\n')[0]


def getStatusCode(header):
    return header[9:12]


# with is easier try catch that auto closes sthings
# AF_INET is address protocol family
def makeRequest(url):
    if 'http://' in url:
        split = url.split('/')
        host = split[2]
        spot = split[3]
    else:
        host = url
        spot = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # SOCK_STREAM specifies we are using TCP
        #s.bind((url, PORT))
        s.connect((host, PORT))
        #addr = s.getaddrinfo()
        req = "GET /{} HTTP/1.1\r\nHost:{}\r\n\r\n".format(spot, host)
        s.send(req.encode('utf-8'))
        # while True:g http://insecure.stevetarzia.com/basic.html u
        #     window = s.recv(4096)
        #     if len(window) == 0:
        #         break
        # response += window
        response = s.recv(4096)

        tempResp = response.decode()
        header = getHeader(tempResp)
        responseCode = getStatusCode(header)
        if responseCode == '200':
            body = getBody(tempResp)
            print(body)
        elif responseCode == '301' or responseCode == '302':
            sys.stderr.write("Redirected to: " + getUrl(header))
            makeRequest(getUrl(header))

        print()
        if response:
            sys.exit(0)
        else:
            sys.exit(1)
        # print(response.decode())

makeRequest(URL)
