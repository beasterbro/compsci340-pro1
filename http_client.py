import socket, requests, sys
exitCode = '400'
url = ''
PORT = 80
# STD out only gets body of response, not headers
# any other message goes to STD err
# listen and send over port 80

url = url
# with is easier try catch that auto closes sthings
# AF_INET is address protocol family
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # SOCK_STREAM specifies we are using TCP
    s.bind((url, PORT))
    s.listen()
    print('Searching for COnnection')
    conn, addr = s.accept()
    with conn:
        print(f'Conncted w/ {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
