from fileinput import filename
import socket
import sys
import os 

files = os.listdir('./')
head ='';
port = int(sys.argv[1])
responseCode = ''
responseStatus = ''

def getResponseCode(req):
    global responseStatus
    split = req.split('HTTP/')
    print(split[0].split(' ')[1][1:])
    print(files)
    requestUrl = split[0].split(' ')[1][1:]
    if requestUrl in files:# If the file exists
        if ('.htm' or '.html') in split[0]:
            return 200
        else:#does not end in not .htm or .html
            responseStatus = 'Forbidden'
            return 403
    else:
        responseStatus = 'Not Found'
        return 404

def makeHeader(body):
    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(body),
        'Connection': 'close',
    }
    global responseCode
    response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
    response_version = 'HTTP/1.1'
    response_status = responseCode
    response_status_text = responseStatus
    # sending all this stuff
    r = '%s %s %s\r\n' % (response_version, response_status, response_status_text)
    r += response_headers_raw
    r+= '\r\n'
    return r

# Create TCP socket to LISTEN for connections-
# BIND that socket to the port provided-
# Listening addr should be "" to listen to all IPs-
# Backlog
# Do this in a loop
    # accept new connections on the accept socket
    # accept return a new socket for connection
    # if file exists construct the http reponse
    # write http header to connection socket and open the file and write its contnets to the connection socket
    # if don't have file makke HTTP error response (404 Not found) and write it to the socket
    # if it does exists bot not correct ending (htm or html) return 403 forbidden
def hostFile():#TODO: Somehow check the file they are requesting for
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # SOCK_STREAM specifies we are using TCP
        s.bind(('', port))#listen to all addresses
        s.listen()
        global responseCode
        while True:
            conn, addr = s.accept()
            req = conn.recv(1024)
            responseCode = getResponseCode(req.decode())
            if responseCode == 200:
                f = open(filename + '.html','r')
                body = f.read()
                print(body)
                head = makeHeader(body)
                conn.send(head.encode(encoding="utf-8"))
                conn.sendall(body.encode(encoding="utf-8"))#Send html response + header
                conn.close()
                sys.exit()

            elif responseCode==403:#400 or the sort
                body = 'Forbidden'
                head = makeHeader(body)
                conn.send(head.encode(encoding="utf-8"))
                conn.sendall(body.encode(encoding="utf-8"))#Send html response + header
                conn.close()
                sys.exit(-1)

            else:#404
                body = 'Not Found'
                head = makeHeader(body)
                conn.send(head.encode(encoding="utf-8"))
                conn.sendall(body.encode(encoding="utf-8"))#Send html response + header
                conn.close()
                sys.exit(-1)

hostFile()