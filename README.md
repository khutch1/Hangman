# Hangman

HANGMAN GAME

To start the server open a unix console and navigate to the directory in 
which the files are located then run startServer.sh with the port number 
provided on the command line e.g.:

bash startServer.sh <port>

Similarly, to start the client navigate to the diretory containing the 
files and run startClient.sh with the host name and port number provided 
on the command line e.g.:

bash startClient.sh <hostname> <port>

This will open up the client in the console and the game may be started 
by typing "START GAME". The server will then choose a secret word and 
respond with dashes for each letter in the word, for example if the 
secret word is "apple" the server will respond with "_____". The server 
out put is outputed to the console on the client side and as the correct 
letters are guessed they are revealed in the server response. When the 
correct word has been guessed the server will respond with a score and 
the "END GAME" message which is shown in the console of the client. 
After this the client may not send any more messages (anything entered 
will result in an error).

The word_list.txt file contains the possible word choices for the game, 
more words may be added to the game by entering a new word on each line 
of this file.
