import socket
import sys
import time
import select
import queue
import os 

files = os.listdir('./')
head ='';
port = int(sys.argv[1])
responseCode = ''
responseStatus = ''
filename = 'rfc2616.html'
def getResponseCode(req):
    global responseStatus
    split = req.split('HTTP/')
    requestUrl = split[0].split(' ')[1][1:]
    if requestUrl in files:# If the file exists
        if ('.htm' or '.html') in split[0]:
            return 200
        else:  # not .htm or .html
            responseStatus = 'Forbidden'
            return 403
    else:
        responseStatus = 'Not Found'
        return 404


def makeHeader(body):
    currentTime = time.ctime(time.time()) + "\r\n"
    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(body),
        'Connection': 'keep-alive',#TODO: do not set to connection close here?
    }
    global responseCode
    response_headers_raw = ''.join('%s: %s\r\n' % (k, v)
                                   for k, v in response_headers.items())
    response_version = 'HTTP/1.1'
    response_status = responseCode
    response_status_text = responseStatus  # this can be random
    # sending all this stuff
    r = '%s %s %s\r\n' % (
        response_version, response_status, response_status_text)
    r += response_headers_raw
    r += '\r\n'
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


def hostFile():  # TODO: Somehow check the file they are requesting for
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # SOCK_STREAM specifies we are using TCP
        s.bind(('', port))  # listen to all addresses
        s.setblocking(False)
        s.listen(5)
        readList = [s]
        outputs = []
        outgoingqueue = {}
        global responseCode
        while readList:
            readable, writable, exceptional = select.select(readList,
                                                    outputs,
                                                    readList)
            # Wait for at least one of the sockets to be
            # ready for processing
            # Handle readList
            for conn in readable:
                if conn is s:
                    # A "readable" socket is ready to accept a connection
                    connection, client_address = conn.accept()
                    print('  connection from', client_address,
                          file=sys.stderr)
                    connection.setblocking(True)
                    readList.append(connection)
                    outgoingqueue[connection] = queue.Queue()
                else:
                    data = conn.recv(1024)
                    if data:
                    # A readable client socket has data
                        processRequest(data,conn)
                        # Add output channel for response
                        if conn not in outputs:
                         outputs.append(conn)
                    else: #no data
                        if conn in outputs:
                            outputs.remove(conn)
                        readList.remove(conn)
                        conn.close()
                        del outgoingqueue[conn]
            # Handle outputs
            for w in writable:
                try:
                    next_msg = outgoingqueue[w].get_nowait()
                except queue.Empty:
                    outputs.remove(w)
                else:
                    conn.send(next_msg)

            # Handle "exceptional conditions"
            for e in exceptional:
                readList.remove(e)
                if e in outputs:
                    outputs.remove(e)
                    e.close()

                # Remove message queue
                del outgoingqueue[e]

def processRequest(data,conn):
    global responseCode
    responseCode = getResponseCode(data.decode())
    if responseCode == 200:
        f = open(filename, 'r')
        body = f.read()
        head = makeHeader(body)
        conn.send(head.encode(encoding="utf-8"))
        # Send html response + header
        conn.sendall(body.encode(encoding="utf-8"))
    elif responseCode == 403:  # 400 or the sort
        body = 'RIP Forbidden'
        head = makeHeader(body)
        conn.send(head.encode(encoding="utf-8"))
        # Send html response + header
        conn.sendall(body.encode(encoding="utf-8"))
    elif responseCode == 404:
        body = 'RIP Not Found'
        head = makeHeader(body)
        conn.send(head.encode(encoding="utf-8"))
        # Send html response + header
        conn.sendall(body.encode(encoding="utf-8"))

hostFile()
