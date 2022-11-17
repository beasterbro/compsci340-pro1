from ast import parse
import socket
import sys
from json.encoder import JSONEncoder
import json


port = int(sys.argv[1])
responseStatus = ''

# GET /product?a=12&b=60& another =0.5
def hasValues(val):
    return any(char.isdigit() for char in val)

def hasValidData(s):
    values = s.split('&')
    va = []
    for v in values:
        if hasValues(v):
            a = v.split('=')
            va.append(float(a[1]))
    return len(va) == len(values)

def getResponseCode(req):
    global responseStatus
    split = req.split('HTTP/')
    print(split) # ['GET /product?a=3&b=7 '
    if '/product' in split[0]:
        parsed = split[0].split('?')
        values = parsed[1] # 'a=3&b=7 '
        print(parsed)
        if hasValidData(values):
            return 200
        else:  # not .htm or .html
            responseStatus = 'Bad Request'
            return 400
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
    response_status_text = responseStatus
    # sending all this stuff
    r = '%s %s %s\r\n' % (
        response_version, response_status, response_status_text)
    r += response_headers_raw
    r += '\r\n'
    return r


def processRequest(req):
    split = req.split('HTTP/')
    parsed = split[0].split('?')
    sv = parsed[1] # 'a=3&b=7 '
    values = sv.split('&')
    va = []
    for v in values:
        a = v.split('=')
        va.append(float(a[1]))
    # ['GET /product?a', '12&b', '60&another', '0.5 ']
    result = 1
    for v in va:
        result *= v
    return va,result

def buildJson(values,product):
    dic = {"operation": "product","operands":values,"result":product}
    return json.dumps(dic,indent=4,separators=(',',': '))


def hostFunction():
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
                val,pro = processRequest(req.decode())
                body = buildJson(val,pro)
                print(body)
                head = makeHeader(body)
                conn.send(head.encode(encoding="utf-8"))
                conn.sendall(body.encode(encoding="utf-8"))#Send html response + header
                conn.close()
                sys.exit()
            else:#400 or the sort
                body = responseStatus
                head = makeHeader(body)
                conn.send(head.encode(encoding="utf-8"))
                conn.sendall(body.encode(encoding="utf-8"))#Send html response + header
                conn.close()
                sys.exit(-1)
hostFunction()