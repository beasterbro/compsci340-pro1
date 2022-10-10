from ast import parse
import socket
import sys
from json.encoder import JSONEncoder
import json


port = int(sys.argv[1])
responseStatus = ''

# GET /product?a=12&b=60& another =0.5
def hasValues(parsed):
    for s in parsed[1:]:
        if not any(char.isdigit() for char in s):
            return False
    return True

def getResponseCode(req):
    global responseStatus
    split = req.split('HTTP/')
    if '/product' in split[0]:
        parsed = split[0].split('=')
        print(parsed)
        if len(parsed) == 4 and hasValues(parsed):
            return 200
        else:  # not .htm or .html
            responseStatus = 'Bad Request'
            return 40
    else:
        responseStatus = 'Not Found'
        return 404


def makeHeader(body):
    response_headers = {
        'Content-Type': 'application/json',
        'Content-Length': len(body),
        'Connection': 'close',
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


def processRequest(req):
    stringRep = req.split('HTTP/')[0].split('=')
    # ['GET /product?a', '12&b', '60&another', '0.5 ']
    values = []
    values.append(float(stringRep[1].split('&')[0]))
    values.append(float(stringRep[2].split('&')[0]))
    values.append(float(stringRep[len(stringRep)-1]))
    return values,values[0]*values[1]*values[2]

def buildJson(values,product):
    dic = {"operation": "product","operands":str(values),"result":product}
    #return JSONEncoder().encode(dic)
    return json.dumps(dic,indent=4,separators=(',',': '))


def hostFunction():#TODO: Somehow check the file they are requesting for
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # SOCK_STREAM specifies we are using TCP
        s.bind(('', port))#listen to all addresses
        s.listen()
        # print(conn)
        global responseCode
        while True:
            conn, addr = s.accept()
            req = conn.recv(1024)
            # print(req.decode())
            responseCode = getResponseCode(req.decode())
            if responseCode == 200:
                val,pro = processRequest(req.decode())
                body = buildJson(val,pro)
                print(body)
                head = makeHeader(body)
                conn.send(head.encode(encoding="utf-8"))
                conn.sendall(body.encode(encoding="utf-8"))#Send html response + header
                conn.close()
            else:#400 or the sort
                body = responseStatus
                head = makeHeader(body)
                conn.send(head.encode(encoding="utf-8"))
                conn.sendall(body.encode(encoding="utf-8"))#Send html response + header
                conn.close()
hostFunction()