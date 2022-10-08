from glob import glob
import socket
import sys
from webbrowser import get

from requests import head

exitCode = '400'
URL = sys.argv[1]  # sys.argv[1]
port = 80
redirectCount = 0
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
    for s in header.split('\n'):
        if "Location: " in s:
            return s[10:]


def getStatusCode(header):
    return header[9:12]


# with is easier try catch that auto closes sthings
# AF_INET is address protocol family
def makeRequest(url):
    if 'http://' in url:
        split = url.split('/')
        host = split[2]
        #cannot do this without threading mutliple ports
        # if ':' in host:
        #     global port
        #     port = int(host.split(':')[1])
        #     host = host.split(':')[0]
        spot = split[3]
    elif 'https://' in url:
        sys.stderr.write("No security allowed >:(")
        sys.exit(-1)
    else:
       # print("else: "+url)
        host = url
        spot = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # SOCK_STREAM specifies we are using TCP
        #s.bind((url, PORT))
        #print(host + '\n')
        s.connect((host, port))
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
        #print(header)
        body = getBody(tempResp)
        if responseCode == '200':
            print(body)
        elif responseCode == '301' or responseCode == '302':
            global redirectCount
            redirectCount+=1
            if redirectCount < 10:
                tempUrl = getUrl(header)
                sys.stderr.write("Redirected to: " + tempUrl)
                makeRequest(tempUrl.split('\r')[0])
            else:
                sys.exit(-1)
        elif int(responseCode) >= 400:
            sys.stderr.write("Error Connecting with response: " + responseCode)
            print(body)
            sys.exit(1)
        if responseCode != '302':
            if responseCode < 400:
                sys.exit(0)
        # print(response.decode())

makeRequest(URL)
