import socket
import sys
import re

#Error function prints reason for exiting
def error(message):
    print(message)
    exit(1)

#function for checking if data is an integer    
def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True
    
#Creating an INET, STREAMing socket
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#checking host and port provided
if sys.argv.__len__() != 3:
   error("Did not provide host and port number.")
else:
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except:
        error("Port number was not and integer.")


#Connecting to server, raises error if unsuccessful
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    error(e)

Response = ''
first_message = True

#Regex for checking for only underscores and lowercase alphabet chars
pattern = r'^[a-z_]+$'

while True:
    #Checks if user wants to start game
    if first_message:
        Input = input('Enter "START GAME" to start: ')
        first_message = False
    #Checks for input (guesses)
    else:
        Input = input('')

    if (Input == ''):
        error("No input provided")
    
    #sends input to server the receives data 
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(256)
    #If there is no data then the program exits with an error
    if not Response:
        error("No server response")
    #decodes and displays data   
    decoded_response = Response.decode('utf-8')
    print(decoded_response)
    """If the server has sent anything that is not a 
    lowercase letter or an underscore, the client assumes
    the game is over, breaks out of the loop and
    closes the connection"""
    if not re.match(pattern, decoded_response):
        break

#Closes client connection
ClientSocket.close()

