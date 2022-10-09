from fileinput import filename
import socket
import sys

port = sys.argv[1]
filename = '/rfc2616.html'

#Create TCP socket to LISTEN for connections
#BIND that socket to the port provided
#Listening addr should be "" to listen to all IPs
#Backlog
#Do this in a loop
    #accept new connections on the accept socket
    #accept return a new socket for connection
    #if file exists construct the http reponse
        #write http header to connection socket and open the file and write its contnets to the connection socket
    #if don't have file makke HTTP error response (404 Not found) and write it to the socket
    #if it does exists bot not correct ending (htm or html) return 403 forbidden