import socket
import sys
import os
import re
from _thread import *
import random

#Error function that prints out reason for server file closing
def error(message):
    print(message)
    sys.exit(1)

#A function to return a random word from the word list
def get_word():
	return random.choice(wordlist).lower()

"""A function that takes in the array of guesses and checks it against
the word then returns the appropriate output string"""
def check(word, guesses):
	status = ''
	for letter in word:
		if letter in guesses:
			status += letter
		else:
			status += '_'
	return status

"""A function for calculating and returning the score if the word is 
guessed"""
def calc_score(word, char_guesses, word_guesses):
	score = len(word)*10 - 2*char_guesses - word_guesses
	return score

#Regex for checking client input consists of only alphabet characters
pattern = r'^[a-z]+$'
#Opens a text file of words and reads it into an array, removes newline characters
my_file = open("word_list.txt", "r")
wordlist = my_file.read().splitlines()

#Creating an INET, STREAMing socket
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Checking that an appropriate argument was provided for the port
if sys.argv.__len__() != 2:
    error("Port number not supplied.")
else:
    try:
        port = int(sys.argv[1])
    except:
        error("Port number was not an integer.")

#Sets the host to that of the current machine
host = socket.gethostname()

#A counter for threads used for testing/error checking
ThreadCount = 0

#Binding the socket to the host and the port
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

#Waiting for a Connection
ServerSocket.listen(5)

#Connection to client
def threaded_client(connection):
    #Buffer set to 256
    data = connection.recv(256)
    #Checking that first message from client is "START GAME"
    first_client_entry = data.decode('utf-8')

    if first_client_entry != "START GAME":
        connection.close()

    else:
        word = get_word()    #Gets random word from list
        guesses = []         #Guesses are stored in array for checking
        guessed = False
        result = check(word, guesses)

        char_guesses = 0    #Storing character and word guesses for calculating score
        word_guesses = 0
        score = 0
        score_string = ''     #Score sent as a string
        
        """puttting a new line character before the 'END GAME' message makes it print on
        a new line after the score on the client side."""
        game_over = "\nGAME OVER"
        

       #Game started
        while True:
            #Sends result should be all '_' to start with
            connection.sendall(str.encode(result))
            #Receives guess, checks that there is data sent
            data = connection.recv(256)
            if not data:
                print('No data.')
                break

	    #Decodes data and sets it to lowercase
            guess = data.decode('utf-8')
            #Converts characters in the client guess to lowercase before checking
            guess = guess.lower()
            #Checks data contains only alphabet characters
            if not re.match(pattern, guess):
                break

	    #Appends guess to array and checks guesses against word
            guesses.append(guess)
            result = check(word, guesses)

            """Checks if guess was a character or word guess
            if the word is guessed breaks out of game loop"""
            if len(guess) > 1:
                word_guesses += 1
                if guess == word:
                    guessed = True
                    break
            elif len(guess) == 1:
                char_guesses += 1
                if result == word:
                    guessed = True
                    break
            else:
                connection.sendall(str.encode(result))
        #If the loop is broken due to a guess (not an error) sends result
        if guessed:
            score = calc_score(word, char_guesses, word_guesses)
            score_string = str(score) + game_over
            connection.sendall(str.encode(score_string))

    #Closes connection to this client
    connection.close()

#Connecting to a new client via a new thread
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

#Closing server socket
ServerSocket.close()
