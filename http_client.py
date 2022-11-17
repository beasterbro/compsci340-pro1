import socket
import sys

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
    return resp.split('\r\n\r\n')[0]


def getBody(resp):
    return resp.split('\r\n\r\n')[1]


def getContentType(header):
     for s in header.split('\n'):
        if "Content-Type: " in s:
            return s

def getUrl(header):
    for s in header.split('\n'):
        if "Location: " in s:
            return s[10:]


def getStatusCode(header):
    return header[9:12]

def isTopLevel(url):
    return len(url.split('/'))<4
# with is easier try catch that auto closes sthings
# AF_INET is address protocol family
def makeRequest(url):
    if  '.jpg' in url:
        sys.stderr.write("No photos allowed >:(")
        sys.exit(-1)
    elif 'http://' in url:
        split = url.split('/')
        host = split[2]
        if ':' in host:
            global port
            port = int(host.split(':')[1])
            host = host.split(':')[0]
        if isTopLevel(url):
            spot = ''
        else:
            spot = '/'.join(split[3:])
    elif 'https://' in url:
        sys.stderr.write("No security allowed >:(")
        sys.exit(-1)
    else:
        host = url
        spot = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#http://insecure.stevetarzia.com/basic.html
        # SOCK_STREAM specifies we are using TCP
        #s.bind((url, PORT))
        #print(host + '\n')
        s.connect((host, port))
        req = "GET /{} HTTP/1.1\r\nHost:{}\r\n\r\n".format(spot, host)
        s.send(req.encode('utf-8'))
        #response = b""
        response = s.recv(1024)

        tempResp = response.decode()
        header = getHeader(tempResp)
        contentType = getContentType(header)
        responseCode = getStatusCode(header)
        body = getBody(tempResp)
        if 'text/html' not in contentType:
            sys.stderr.write("Incorrect Content type: " + contentType)
            sys.exit(-1)
        if responseCode == '200':
            print(body)
            pass
        elif responseCode == '301' or responseCode == '302':
            global redirectCount
            redirectCount+=1
            if redirectCount < 10:
                tempUrl = getUrl(header)
                sys.stderr.write("Redirected to: " + tempUrl + '\n')
                makeRequest(tempUrl.split('\r')[0])
                sys.exit(0)
            else:
                sys.exit(-1)
        elif int(responseCode) >= 400:
            sys.stderr.write("Error Connecting with response: " + responseCode)
            print(body)
            sys.exit(1)
        if responseCode != '302':
            if int(responseCode) < 400:
                sys.exit(0)

makeRequest(URL)
